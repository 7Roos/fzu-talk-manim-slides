from manim import *
from components.custom_slide import CustomSlide


class Slide8(CustomSlide):
    def construct(self):
        title = Text(
            "Conclusion",
            font="DejaVu Sans",
            weight=BOLD,
            font_size=self.FONT_SIZE_SUBTITLE,
            color=self.get_color("title"),
        ).to_edge(UP)

        spinDown = self.get_color("line", category="timeline")
        spinUP = self.get_color("highlight")

        consequences = (
            VGroup(
                Text(
                    "- Reduction of ordering temperature;",
                    font_size=self.FONT_SIZE_TEXT,
                    color=spinDown,
                ),
                Text(
                    "- Rich phase diagram;",
                    font_size=self.FONT_SIZE_TEXT,
                    color=self.get_color("secondary"),
                ),
                Text(
                    "- Ground-state degeneracy;",
                    font_size=self.FONT_SIZE_TEXT,
                    color=spinDown,
                ),
                Text(
                    "- Residual entropy;",
                    font_size=self.FONT_SIZE_TEXT,
                    color=self.get_color("secondary"),
                ),
                Text(
                    "- Macroscopic degeneracy;",
                    font_size=self.FONT_SIZE_TEXT,
                    color=spinDown,
                ),
                Text(
                    "- Non-trivial phases.",
                    font_size=self.FONT_SIZE_TEXT,
                    color=self.get_color("secondary"),
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .to_edge(LEFT)
        )

        self.add(title, consequences[0])
        self.wait(0.5)
        for item in range(1, len(consequences)):
            self.next_slide()
            self.add(consequences[item])
            self.wait()