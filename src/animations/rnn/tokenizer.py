"""Step-by-step Manim explainer for the from-scratch tokenizer.

Visualises the pipeline described in ``docs/rnn/tokenizer.md`` for the
English -> Bengali translation task: dataset -> normalize -> tokenize ->
build vocabulary -> encode -> decode -> pad -> ready for training.

The numeric example traced through the scene matches the tutorial exactly::

    "i like math ."  ->  ["i", "like", "math", "."]  ->  [2, 7, 9, 11, 4, 3]

Render (high quality, preview)::

    make render SCENE=src/animations/rnn/tokenizer.py:TokenizerPipeline
    # or directly:
    uv run manim -pqh src/animations/rnn/tokenizer.py TokenizerPipeline

Quick draft while iterating::

    uv run manim -pql src/animations/rnn/tokenizer.py TokenizerPipeline
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    Arrow,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    Line,
    RoundedRectangle,
    Scene,
    Square,
    Text,
    Transform,
    VGroup,
    Write,
)

# --- Palette -----------------------------------------------------------------
BG = "#0f1117"
WORD = "#4ea8de"  # regular word tokens
IDCOL = "#90be6d"  # integer ids
SPECIAL = "#f9c74f"  # <PAD> <UNK> <SOS> <EOS>
SOS = "#43aa8b"
EOS = "#f94144"
PAD = "#8d99ae"
ACCENT = "#c77dff"
MUTED = "#6c757d"

BENGALI_FONT = "Baloo Da 2"  # ships with macOS, has Bengali glyphs

TOTAL_STEPS = 7

# English vocabulary exactly as build_vocab() produces it (specials + sorted).
VOCAB = [
    "<PAD>",  # 0
    "<UNK>",  # 1
    "<SOS>",  # 2
    "<EOS>",  # 3
    ".",  # 4
    "ai",  # 5
    "deep",  # 6
    "i",  # 7
    "learning",  # 8
    "like",  # 9
    "love",  # 10
    "math",  # 11
]


def token_box(
    label: str,
    color: str,
    *,
    font_size: int = 30,
    min_width: float = 1.0,
    height: float = 0.85,
) -> VGroup:
    """A rounded pill containing a token string."""
    text = Text(label, font_size=font_size, color=WHITE)
    width = max(text.width + 0.5, min_width)
    box = RoundedRectangle(
        corner_radius=0.14,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=0.16,
    )
    text.move_to(box)
    return VGroup(box, text)


def id_box(value: int, color: str = IDCOL, *, side: float = 0.85) -> VGroup:
    """A small square holding an integer id."""
    text = Text(str(value), font_size=30, color=WHITE)
    box = Square(
        side_length=side,
        stroke_color=color,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=0.18,
    )
    text.move_to(box)
    return VGroup(box, text)


class TokenizerPipeline(Scene):
    """The full nine-part explainer, played end to end."""

    def construct(self) -> None:
        self.camera.background_color = BG  # type: ignore[union-attr]
        self._build_header()

        self.intro()
        self.step_1_dataset()
        self.step_2_normalize()
        self.step_3_tokenize()
        self.step_4_vocabulary()
        self.step_5_encode()
        self.step_6_decode()
        self.step_7_pad()
        self.outro()

    # -- header / chrome ------------------------------------------------------
    def _build_header(self) -> None:
        self.step_label = Text("", font_size=22, color=ACCENT).to_corner(UP + LEFT)
        self.title_text = Text("", font_size=34, color=WHITE).to_edge(UP)
        self.rule = Line(LEFT * 6.6, RIGHT * 6.6, stroke_color=MUTED, stroke_width=1.5)
        self.rule.next_to(self.title_text, DOWN, buff=0.18)
        self.header = VGroup(self.step_label, self.title_text, self.rule)
        self.add(self.header)

    def section(self, step: int, title: str) -> None:
        """Fade out the current body and retitle the header for a new step."""
        keep = {self.step_label, self.title_text, self.rule, self.header}
        body = [m for m in self.mobjects if m not in keep]
        if body:
            self.play(*[FadeOut(m) for m in body], run_time=0.6)

        new_label = Text(
            f"STEP {step} / {TOTAL_STEPS}", font_size=22, color=ACCENT
        ).to_corner(UP + LEFT)
        new_title = Text(title, font_size=34, color=WHITE).to_edge(UP)
        new_rule = Line(
            LEFT * 6.6, RIGHT * 6.6, stroke_color=MUTED, stroke_width=1.5
        ).next_to(new_title, DOWN, buff=0.18)
        self.play(
            Transform(self.step_label, new_label),
            Transform(self.title_text, new_title),
            Transform(self.rule, new_rule),
            run_time=0.6,
        )

    def caption(self, text: str, color: str = MUTED) -> Text:
        cap = Text(text, font_size=24, color=color).to_edge(DOWN, buff=0.6)
        return cap

    # -- intro ----------------------------------------------------------------
    def intro(self) -> None:
        title = Text("Building a Tokenizer", font_size=52, color=WHITE)
        subtitle = Text(
            "English  →  Bengali  ·  from scratch, no libraries",
            font_size=28,
            color=WORD,
        )
        subtitle.next_to(title, DOWN, buff=0.35)
        group = VGroup(title, subtitle).move_to(UP * 1.2)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)

        stages = ["Raw", "Normalize", "Tokenize", "Vocab", "Encode", "Pad", "Ready"]
        chips = VGroup()
        for name in stages:
            chip = token_box(name, WORD, font_size=22, min_width=1.1, height=0.7)
            chips.add(chip)
        chips.arrange(RIGHT, buff=0.5).scale_to_fit_width(12.0)
        chips.next_to(group, DOWN, buff=1.0)

        arrows = VGroup()
        for a, b in zip(chips[:-1], chips[1:], strict=False):
            arrows.add(
                Arrow(
                    a.get_right(),
                    b.get_left(),
                    buff=0.08,
                    stroke_width=3,
                    color=MUTED,
                    max_tip_length_to_length_ratio=0.4,
                )
            )

        self.play(FadeIn(chips[0]))
        for chip, arrow in zip(chips[1:], arrows, strict=False):
            self.play(GrowArrow(arrow), FadeIn(chip), run_time=0.35)
        self.wait(1.0)

    # -- step 1 ---------------------------------------------------------------
    def step_1_dataset(self) -> None:
        self.section(1, "Define the Dataset")

        english = ["I like math .", "I like learning AI .", "I love deep learning ."]
        bengali = [
            "আমি গণিত পছন্দ করি ।",
            "আমি এআই শিখতে পছন্দ করি ।",
            "আমি ডিপ লার্নিং ভালোবাসি ।",
        ]

        rows = VGroup()
        for en, bn in zip(english, bengali, strict=False):
            en_t = Text(en, font_size=28, color=WHITE)
            arrow = Text("→", font_size=28, color=MUTED)
            bn_t = Text(bn, font_size=28, color=WORD, font=BENGALI_FONT)
            row = VGroup(en_t, arrow, bn_t).arrange(RIGHT, buff=0.5)
            rows.add(row)
        rows.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(DOWN * 0.2)

        cap = self.caption("Three sentence pairs — tiny, but enough to see every step.")

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.5)
        self.play(FadeIn(cap))
        self.wait(1.2)

    # -- step 2 ---------------------------------------------------------------
    def step_2_normalize(self) -> None:
        self.section(2, "Normalize the Text")

        before = Text("I Like Math .", font_size=40, color=WHITE)
        after = Text("i like math .", font_size=40, color=WORD)
        before.move_to(UP * 0.8)
        after.move_to(DOWN * 0.8)

        arrow = Arrow(before.get_bottom(), after.get_top(), buff=0.25, color=ACCENT)
        label = Text(".lower().strip()", font_size=24, color=ACCENT)
        label.next_to(arrow, RIGHT, buff=0.3)

        cap = self.caption("Lowercasing collapses Math / MATH / math into one token.")

        self.play(Write(before))
        self.play(GrowArrow(arrow), FadeIn(label))
        self.play(Transform(before.copy(), after), FadeIn(after))
        self.play(FadeIn(cap))
        self.wait(1.2)

    # -- step 3 ---------------------------------------------------------------
    def step_3_tokenize(self) -> None:
        self.section(3, "Tokenize (whitespace split)")

        sentence = Text("i like math .", font_size=40, color=WHITE).move_to(UP * 1.2)
        arrow = Text("split()  ↓", font_size=26, color=ACCENT).move_to(UP * 0.1)

        tokens = ["i", "like", "math", "."]
        pills = VGroup(*[token_box(t, WORD) for t in tokens])
        pills.arrange(RIGHT, buff=0.4).move_to(DOWN * 1.0)

        cap = self.caption('sentence.split()  →  ["i", "like", "math", "."]')

        self.play(Write(sentence))
        self.play(FadeIn(arrow))
        self.play(
            *[FadeIn(p, shift=DOWN * 0.2) for p in pills],
            lag_ratio=0.15,
            run_time=1.0,
        )
        self.play(FadeIn(cap))
        self.wait(1.2)

    # -- step 4 ---------------------------------------------------------------
    def step_4_vocabulary(self) -> None:
        self.section(4, "Build the Vocabulary")

        entries = VGroup()
        for idx, tok in enumerate(VOCAB):
            is_special = tok.startswith("<")
            col = SPECIAL if is_special else WORD
            num = Text(f"{idx:>2}", font_size=24, color=IDCOL)
            box = token_box(tok, col, font_size=24, min_width=1.6, height=0.6)
            entry = VGroup(num, box).arrange(RIGHT, buff=0.3)
            entries.add(entry)

        left = VGroup(*entries[:6]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        right = VGroup(*entries[6:]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        columns = VGroup(left, right).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.3)

        legend = VGroup(
            token_box("special", SPECIAL, font_size=20, min_width=1.6, height=0.5),
            token_box("word", WORD, font_size=20, min_width=1.4, height=0.5),
        ).arrange(RIGHT, buff=0.5)
        legend.next_to(columns, UP, buff=0.4).to_edge(RIGHT, buff=1.0)

        cap = self.caption(
            "4 special tokens first, then the unique words sorted — each gets an id."
        )

        self.play(FadeIn(legend))
        self.play(
            *[FadeIn(e, shift=RIGHT * 0.2) for e in entries],
            lag_ratio=0.08,
            run_time=1.6,
        )
        # Highlight the special block
        self.play(*[Indicate(entries[i], color=SPECIAL) for i in range(4)])
        self.play(FadeIn(cap))
        self.wait(1.0)

    # -- step 5 ---------------------------------------------------------------
    def step_5_encode(self) -> None:
        self.section(5, "Encode Tokens → IDs")

        tokens = ["i", "like", "math", "."]
        ids = [7, 9, 11, 4]

        pills = VGroup(*[token_box(t, WORD) for t in tokens])
        pills.arrange(RIGHT, buff=0.5).move_to(UP * 1.6)

        id_row = VGroup(*[id_box(i) for i in ids])
        for pill, box in zip(pills, id_row, strict=False):
            box.next_to(pill, DOWN, buff=1.1)

        arrows = VGroup(
            *[
                Arrow(
                    p.get_bottom(), b.get_top(), buff=0.12, color=MUTED, stroke_width=3
                )
                for p, b in zip(pills, id_row, strict=False)
            ]
        )

        self.play(FadeIn(pills, shift=DOWN * 0.2))
        self.play(
            *[GrowArrow(a) for a in arrows],
            *[FadeIn(b, shift=DOWN * 0.2) for b in id_row],
            lag_ratio=0.1,
            run_time=1.2,
        )
        self.wait(0.4)

        # Wrap with <SOS> ... <EOS>: transform the real id boxes into their slots.
        target = VGroup(id_box(2, SOS), *[id_box(i) for i in ids], id_box(3, EOS))
        target.arrange(RIGHT, buff=0.35).move_to(DOWN * 0.6)
        sos_lbl = Text("<SOS>", font_size=20, color=SOS)
        sos_lbl.next_to(target[0], DOWN, buff=0.2)
        eos_lbl = Text("<EOS>", font_size=20, color=EOS)
        eos_lbl.next_to(target[-1], DOWN, buff=0.2)

        self.play(FadeOut(pills), FadeOut(arrows))
        self.play(
            *[Transform(id_row[i], target[i + 1]) for i in range(len(ids))],
            FadeIn(target[0], shift=RIGHT * 0.3),
            FadeIn(target[-1], shift=LEFT * 0.3),
            FadeIn(sos_lbl),
            FadeIn(eos_lbl),
            run_time=1.0,
        )

        result = Text("[2, 7, 9, 11, 4, 3]", font_size=32, color=IDCOL)
        result.to_edge(DOWN, buff=0.7)
        self.play(Write(result))
        self.wait(1.2)

    # -- step 6 ---------------------------------------------------------------
    def step_6_decode(self) -> None:
        self.section(6, "Decode IDs → Tokens")

        ids = [2, 7, 9, 11, 4, 3]
        colors = [SOS, IDCOL, IDCOL, IDCOL, IDCOL, EOS]
        id_row = VGroup(*[id_box(i, c) for i, c in zip(ids, colors, strict=False)])
        id_row.arrange(RIGHT, buff=0.4).move_to(UP * 1.2)

        toks = ["<SOS>", "i", "like", "math", ".", "<EOS>"]
        tok_cols = [SOS, WORD, WORD, WORD, WORD, EOS]
        pills = VGroup(
            *[
                token_box(t, c, font_size=24, min_width=1.2)
                for t, c in zip(toks, tok_cols, strict=False)
            ]
        )
        for pill, box in zip(pills, id_row, strict=False):
            pill.next_to(box, DOWN, buff=1.1)

        arrows = VGroup(
            *[
                Arrow(
                    b.get_bottom(), p.get_top(), buff=0.12, color=MUTED, stroke_width=3
                )
                for b, p in zip(id_row, pills, strict=False)
            ]
        )

        cap = self.caption("id_to_token lookup — handy for reading model output.")

        self.play(FadeIn(id_row))
        self.play(
            *[GrowArrow(a) for a in arrows],
            *[FadeIn(p, shift=DOWN * 0.2) for p in pills],
            lag_ratio=0.1,
            run_time=1.4,
        )
        self.play(FadeIn(cap))
        self.wait(1.2)

    # -- step 7 ---------------------------------------------------------------
    def step_7_pad(self) -> None:
        self.section(7, "Pad the Sequences")

        seq_a = [2, 7, 9, 11, 4, 3]
        seq_b = [2, 7, 9, 8, 5, 4, 3]

        row_a = VGroup(*[id_box(i) for i in seq_a]).arrange(RIGHT, buff=0.3)
        row_b = VGroup(*[id_box(i) for i in seq_b]).arrange(RIGHT, buff=0.3)
        row_a.move_to(UP * 1.1)
        row_b.next_to(row_a, DOWN, buff=0.7, aligned_edge=LEFT)

        len_a = Text("len 6", font_size=22, color=MUTED).next_to(row_a, LEFT, buff=0.4)
        len_b = Text("len 7", font_size=22, color=MUTED).next_to(row_b, LEFT, buff=0.4)

        self.play(FadeIn(row_a), FadeIn(row_b), FadeIn(len_a), FadeIn(len_b))
        self.wait(0.4)

        # Append a <PAD> (id 0) to the shorter sequence.
        pad = id_box(0, PAD).next_to(row_a[-1], RIGHT, buff=0.3)
        pad_lbl = Text("<PAD>", font_size=20, color=PAD).next_to(pad, UP, buff=0.2)

        new_len = Text("len 7", font_size=22, color=IDCOL).move_to(len_a)
        self.play(FadeIn(pad, shift=LEFT * 0.3), FadeIn(pad_lbl))
        self.play(Indicate(pad, color=PAD), Transform(len_a, new_len))

        cap = self.caption("Every sequence in a batch now shares one length.")
        self.play(FadeIn(cap))
        self.wait(1.2)

    # -- outro ----------------------------------------------------------------
    def outro(self) -> None:
        keep = {self.step_label, self.title_text, self.rule, self.header}
        body = [m for m in self.mobjects if m not in keep]
        self.play(
            *[FadeOut(m) for m in body],
            FadeOut(self.header),
            run_time=0.6,
        )

        title = Text("Ready for Training", font_size=48, color=WHITE).move_to(UP * 2.2)

        enc = VGroup(*[id_box(i) for i in [2, 7, 9, 11, 4, 3, 0]]).arrange(
            RIGHT, buff=0.3
        )
        enc_lbl = Text("Encoder Input", font_size=24, color=WORD).next_to(
            enc, LEFT, buff=0.5
        )
        enc_group = VGroup(enc_lbl, enc).move_to(UP * 0.4)

        tgt = VGroup(*[id_box(i, ACCENT) for i in [2, 4, 7, 9, 6, 13, 3]]).arrange(
            RIGHT, buff=0.3
        )
        tgt_lbl = Text("Target Output", font_size=24, color=ACCENT).next_to(
            tgt, LEFT, buff=0.5
        )
        tgt_group = VGroup(tgt_lbl, tgt).next_to(enc_group, DOWN, buff=0.7)
        VGroup(enc_group, tgt_group).move_to(UP * 0.3)

        arrow = Arrow(UP * 0.9, DOWN * 1.6, color=MUTED, stroke_width=4)
        arrow.next_to(tgt_group, DOWN, buff=0.4)
        tensor = Text("→  Tensor  →  Encoder", font_size=30, color=IDCOL)
        tensor.next_to(arrow, DOWN, buff=0.3)

        self.play(Write(title))
        self.play(FadeIn(enc_group, shift=UP * 0.2))
        self.play(FadeIn(tgt_group, shift=UP * 0.2))
        self.play(GrowArrow(arrow), FadeIn(tensor))
        self.play(Indicate(VGroup(enc, tgt), color=IDCOL))
        self.wait(2.0)
