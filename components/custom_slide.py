from manim import *
from manim_slides import Slide
#from manim import AS2700
import numpy as np


# Subclass Custom Scenes
# MovingCameraSlide herda funcionalidades tanto de Slide
# (do manim-slides) quanto de MovingCameraScene (do Manim).
class MovingCameraSlide(Slide, MovingCameraScene):
    pass


class CustomSlide(Slide):
    """Classe base personalizada para slides"""

    # Paletas de cores para temas claro e escuro
    PALETTE = {
        "light": {
            "background": "#FFFFFF",
            "text": "#333333",
            "title": "#023020",  # Dark green
            "emphasis": "#C0392B",  # Vermelho
            "primary": "#1A5276",  # Azul
            "secondary": "#16A085",  # Verde
            "tertiary": "#8E44AD",  # Roxo
            "highlight": "#F39C12",  # Laranja
            "divider": "#353333",  # Cinza claro
            "transparent": "#FFFFFF00",  # Branco transparente
            "success": "#27AE60",  # Verde escuro
            "warning": "#F1C40F",  # Amarelo
            "error": "#E74C3C",  # Vermelho claro
            # Cores para gráficos e visualizações
            "graph": {
                "axes": "#7F8C8D",
                "grid": "#ECEFF1",
                "series1": "#3498DB",
                "series2": "#E74C3C",
                "series3": "#2ECC71",
                "series4": "#F1C40F",
                "series5": "#9B59B6",
            },
            # Cores para a linha do tempo
            "timeline": {
                "line": "#003963",  # Azul escuro
                "marker": "#FBC948",
                "highlight": "#FBC948",
                "text": "#E5E5E5",
                "shadow": "#00000033",  # Sombra leve
            },
        },
        "dark": {
            "background": "#121212",
            "text": "#EEEEEE",
            "title": "#4FC3F7",  # Azul claro
            "emphasis": "#FF5252",  # Vermelho
            "primary": "#64B5F6",  # Azul
            "secondary": "#4DB6AC",  # Verde
            "tertiary": "#BA68C8",  # Roxo
            "highlight": "#FFB74D",  # Laranja
            "divider": "#353333",  # Cinza
            "transparent": "#00000000",  # Preto transparente
            "success": "#66BB6A",  # Verde
            "warning": "#FFCA28",  # Amarelo
            "error": "#EF5350",  # Vermelho
            # Cores para gráficos e visualizações
            "graph": {
                "axes": "#9E9E9E",
                "grid": "#424242",
                "series1": "#64B5F6",
                "series2": "#FF5252",
                "series3": "#4DB6AC",
                "series4": "#FFB74D",
                "series5": "#BA68C8",
            },
            # Cores para a linha do tempo
            "timeline": {
                "line": "#DB611D",
                "marker": "#FBC948",
                "highlight": "#FFB74D",
                "text": "#EEEEEE",
                "shadow": "#00000080",
            },
        },
    }

    # Cores convertidas para formatos Manim - será preenchido em runtime
    COLORS = {}

    # Tema atual (light ou dark)
    current_theme = "light"  # Padrão: tema escuro

    # Adicione o valor TOTAL_SLIDES como atributo de classe
    TOTAL_SLIDES = 27  # Ajuste este número conforme a quantidade de slides

    # Tamanhos de fonte por tipo de elemento
    FONT_SIZE_TITLE = 60  # Títulos principais
    FONT_SIZE_SUBTITLE = 40  # Subtítulos
    FONT_SIZE_HEADING = 32  # Cabeçalhos de seção
    FONT_SIZE_TEXT = 24  # Texto principal/corpo
    FONT_SIZE_CAPTION = 28  # Caption das figuras
    FONT_SIZE_FOOTNOTE = 16  # Notas de rodapé/referências
    FONT_SIZE_GRAPH_LABEL = 20  # Rótulos de gráficos
    # Tamanhos específicos para elementos matemáticos
    FONT_SIZE_EQ = 50  # Equações grandes/destacadas
    FONT_SIZE_EQ_TEXT = 35  # Texto em equações
    FONT_SIZE_INLINE_MATH = 28  # Matemática em linha com texto
    FONT_SIZE_GRAPH_LABEL_MATH = 30  # Rótulos de gráficos
    # Tamanhos para elementos especiais
    FONT_SIZE_CITATION = 16  # Citações
    FONT_SIZE_SLIDE_NUMBER = 25  # Número do slide
    FONT_SIZE_CODE = 22  # Código-fonte
    # Família de fontes
    FONT_SANS_SERIF = "Asap"
    FONT_SERIF = "Antykwa Torunska"

    # Flag para controlar se a numeração deve ser mostrada
    show_slide_numbers = True

    # Contador global de slides - mantido como variável de classe
    current_slide = 1

    # Contador global de referências
    current_reference = 0

    # Dicionário global de referências para compartilhar entre slides
    REFERENCES = {}

    # Contador global de figuras/captionss
    current_figure = 0

    # Template LaTeX global (será configurado pelo presentation.py)
    global_tex_template = None

    def __init__(self, *args, **kwargs):
        # Extrair opções específicas antes de passar para a superclasse
        self.show_slide_numbers = kwargs.pop("show_slide_numbers", True)
        super().__init__(*args, **kwargs)

        # Converte cores hexadecimais para formatos Manim
        self._initialize_colors()

        self.skip_reversing = True  # Desabilita reversão automática de animações

        # Configurar template LaTeX global com pacotes necessários
        self._setup_tex_template()

        # Background color
        self.set_theme(self.current_theme)

    def _initialize_colors(self):
        """Converte cores hex da paleta para objetos de cor Manim"""
        for theme in ["light", "dark"]:
            self.COLORS[theme] = {}

            # Converter cores principais
            for key, value in self.PALETTE[theme].items():
                if isinstance(value, dict):
                    # Para subcategorias (como "graph" e "timeline")
                    self.COLORS[theme][key] = {}
                    for subkey, color_str in value.items():
                        if isinstance(color_str, str):
                            self.COLORS[theme][key][subkey] = ManimColor.from_hex(
                                color_str
                            )
                elif isinstance(value, str):
                    self.COLORS[theme][key] = ManimColor.from_hex(value)

    def _setup_tex_template(self):
        """Configura um template LaTeX com pacotes necessários"""
        # Usar template global se disponível (configurado por presentation.py)
        if CustomSlide.global_tex_template is not None:
            self.myTemplate = CustomSlide.global_tex_template
        else:
            # Fallback: criar template local se não houver global
            self.myTemplate = TexTemplate()
            self.myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
            # Adicione outros pacotes conforme necessário
            # self.myTemplate.add_to_preamble(r"\usepackage{amsmath}")
            # self.myTemplate.add_to_preamble(r"\usepackage{amssymb}")

    def set_theme(self, theme="dark"):
        """Define o tema de cores (light ou dark)"""
        if theme in ["light", "dark"]:
            self.current_theme = theme
            # Define a cor de fundo com base no tema
            background_color = self.COLORS[theme]["background"]
            self.camera.background_color = background_color
        else:
            print(f"Tema '{theme}' não reconhecido. Use 'light' ou 'dark'.")

    def get_color(self, color_name, category=None):
        """
        Obtém uma cor da paleta atual

        Args:
            color_name: Nome da cor (ex: "primary", "text")
            category: Categoria opcional (ex: "graph", "timeline")

        Returns:
            Color: Objeto de cor Manim
        """
        if category:
            try:
                color = self.COLORS[self.current_theme][category][color_name]

                return color
                # return self.COLORS[self.current_theme][category][color_name]
            except Exception as e:
                print(f"CustomSlide.get_color: Erro ao obter cor: {e}")
                return WHITE  # Cor padrão em caso de erro
        else:
            try:
                color = self.COLORS[self.current_theme][color_name]
                return color
            except KeyError:
                print(f"Cor '{color_name}' não encontrada no tema atual")
                return WHITE

    def next_slide(self, update_number=False, loop=False):
        """
        Avança para o próximo slide com opção de atualizar ou não a numeração.

        Args:
            update_number (bool): Se True, incrementa o contador de slides. Default: False.
            loop (bool): Se True, o slide entra em modo de loop. Default: False.
        """
        # Primeiro chama o método original da classe Slide para pausa na apresentação
        # Passa o parâmetro loop para o método da superclasse
        super().next_slide(loop=loop)

        # Só atualiza a numeração se explicitamente solicitado
        if update_number and self.show_slide_numbers and hasattr(self, "slide_counter"):
            # Atualiza o contador de slides
            self.slide_counter += 1

            # Atualiza o número do slide na tela
            self._update_slide_number_display()

    def setup_scene(self):
        """Método chamado automaticamente antes de construct() para configurar a cena"""
        # Este método é executado antes de construct(), sendo ideal para inicializações

        # Define slide_counter para este slide específico
        # Começa do 1 se for a primeira vez que o método é chamado
        CustomSlide.current_slide += 1
        self.slide_counter = CustomSlide.current_slide

        # Se a numeração estiver ativada, adiciona o número do slide
        if self.show_slide_numbers:
            self._setup_slide_number()

    def _setup_slide_number(self):
        """Configuração interna da numeração de slides"""
        # Cria o texto com o número do slide
        slide_number = Text(
            f"{self.slide_counter}/{self.TOTAL_SLIDES}",
            font_size=self.FONT_SIZE_SLIDE_NUMBER,
            color=self.get_color("text"),
        ).to_corner(UR)

        # Adiciona ao canvas usando o método herdado da classe Slide
        self.add_to_canvas(slide_number=slide_number)

        # Adiciona à cena para que seja visível imediatamente
        self.add(slide_number)

    def _update_slide_number_display(self):
        """Atualiza o texto do número do slide"""
        if "slide_number" in self.canvas:
            old_number = self.canvas["slide_number"]
            new_number = Text(
                f"{self.slide_counter}/{self.TOTAL_SLIDES}",
                font_size=self.FONT_SIZE_SLIDE_NUMBER,
                color=self.get_color("text"),
            ).move_to(old_number)

            self.play(Transform(old_number, new_number), run_time=0.5)
            self.wait(0.1)

    def transition_out(self, direction=UP):
        """Move all mobjects out of the screen in the specified direction"""
        # Agrupa todos os objetos na cena
        all_mobjects = Group(*self.mobjects)
        self.clear()
        # Avoid clear slide_number
        if hasattr(self, "canvas") and "slide_number" in self.canvas:
            self.add(self.canvas["slide_number"])
        self.wait(0.5)

    '''
    Citações e referências    
    def cite(self, obj, author, title, year, journal=None, doi=None):
        """
        Adiciona uma citação e retorna um número de referência formatado.

        Args:
            obj: O objeto Manim ao qual a citação está associada
            author: Autor(es) da referência
            title: Título da publicação
            year: Ano da publicação
            journal: Nome do periódico (opcional)
            doi: DOI da publicação (opcional)

        Returns:
            VGroup: Contém o número da referência formatado como sobrescrito
        """
        # Incrementa o contador global de referências
        CustomSlide.current_reference += 1
        ref_num = CustomSlide.current_reference

        # Armazena os dados da referência no dicionário global
        CustomSlide.REFERENCES[ref_num] = {
            "author": author,
            "title": title,
            "year": year,
            "journal": journal,
            "doi": doi,
            "object": obj,
        }

        # Cria o número de citação formatado (sobrescrito)
        citation_num = Text(
            f"[{ref_num}]",
            font_size=self.FONT_SIZE_CITATION,
            color=self.get_color("series1", "graph"),
        ).scale(0.8)

        # Posiciona o número como sobrescrito junto ao objeto
        if isinstance(obj, BulletedList):
            # Para BulletedList, é um caso especial que precisa de ajuste específico
            citation_num.next_to(obj, RIGHT).shift(0.36 * LEFT + 0.2 * UP)
        else:
            # Para outros objetos, posiciona à direita
            citation_num.next_to(obj, RIGHT).shift(0.1 * UP)

        # Adicionar o número da referência como atributo do objeto
        citation_num.ref_number = ref_num

        return citation_num

    def get_current_slide_references(self):
        """
        Retorna uma lista com os números das referências criadas especificamente neste slide.
        Útil para criar rodapés apenas com as referências relevantes ao slide atual.

        Returns:
            list: Lista de números de referências do slide atual
        """
        # Esta implementação pressupõe que você mantenha controle das referências por slide
        # Como alternativa simples, vamos criar um método para coletar referências recentes
        if not hasattr(self, "_slide_references"):
            self._slide_references = []
        return self._slide_references

    def track_reference(self, citation_obj):
        """
        Registra uma referência como pertencente ao slide atual.

        Args:
            citation_obj: Objeto retornado pelo método cite()
        """
        if not hasattr(self, "_slide_references"):
            self._slide_references = []

        if hasattr(citation_obj, "ref_number"):
            self._slide_references.append(citation_obj.ref_number)

    def create_footer_for_slide_references(self, full=False):
        """
        Cria rodapé apenas com as referências rastreadas neste slide.

        Args:
            full (bool): Se True, inclui título completo na referência

        Returns:
            VGroup: Rodapé com referências do slide atual
        """
        slide_refs = self.get_current_slide_references()
        return self.create_footer_references(reference_numbers=slide_refs, full=full)

    def create_references_slide(self, title="Referências"):
        """
        Cria um slide de referências formatado.

        Args:
            title: Título do slide de referências
        """
        # Configurar fundo
        self.setup_background()

        # Título
        references_title = Text(
            title, font_size=40, color=self.get_color("title")
        ).to_edge(UP)
        self.add(references_title)

        # Lista de referências
        references_list = VGroup()

        for ref_num, ref_data in sorted(CustomSlide.REFERENCES.items()):
            # Formata a referência no estilo acadêmico
            journal_text = f", {ref_data['journal']}" if ref_data.get("journal") else ""
            doi_text = f", DOI: {ref_data['doi']}" if ref_data.get("doi") else ""

            ref_text = f"[{ref_num}] {ref_data['author']} ({ref_data['year']}). {ref_data['title']}{journal_text}{doi_text}."

            reference = Text(
                ref_text, font_size=22, color=self.get_color("text"), line_spacing=0.8
            )

            references_list.add(reference)

        # Organizar as referências
        references_list.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        references_list.scale(0.9).to_edge(LEFT).shift(RIGHT + DOWN * 0.5)

        # Adicionar referências ao slide
        self.play(Write(references_list), run_time=2)

        # Adicionar número do slide
        self.next_slide(update_number=True)

    def show_citation(self, citation_num, fade_in=True, animate=True):
        """
        Mostra um número de citação no slide

        Args:
            citation_num: O objeto de citação retornado por self.cite()
            fade_in: Se True, usa animação FadeIn
            animate: Se True, usa animação, senão apenas adiciona à cena
        """
        if animate:
            if fade_in:
                self.play(FadeIn(citation_num, scale=1.2), run_time=0.3)
            else:
                self.play(Write(citation_num), run_time=0.3)
        else:
            self.add(citation_num)

    def create_footer_references(self, reference_numbers=None, full=False):
        """
        Cria uma linha de rodapé com referências formatadas para o slide atual.

        Args:
            reference_numbers (list, optional): Lista de números de referências específicas.
                                               Se None, mostra todas as referências. Default: None
            full (bool, optional): Se True, inclui o título na referência. Default: False

        Returns:
            VGroup: Um grupo contendo as referências formatadas especificadas.

        Example:
            # Mostrar apenas a referência atual
            footer = self.create_footer_references([citation2.get_ref_number()])

            # Mostrar referências específicas
            footer = self.create_footer_references([1, 3, 5])

            # Mostrar todas as referências (comportamento original)
            footer = self.create_footer_references()
        """
        footer_refs = VGroup()

        # Se reference_numbers não for especificado, usar todas as referências
        if reference_numbers is None:
            refs_to_show = CustomSlide.REFERENCES.items()
        else:
            # Filtrar apenas as referências especificadas
            refs_to_show = [
                (num, CustomSlide.REFERENCES[num])
                for num in reference_numbers
                if num in CustomSlide.REFERENCES
            ]

        for ref_num, ref_data in sorted(refs_to_show):
            if full:
                ref_text = f"[{ref_num}] {ref_data['author']}, \"{ref_data['title']}\" ({ref_data['year']})."
            else:
                ref_text = f"[{ref_num}] {ref_data['author']} ({ref_data['year']})."

            footer_ref = Text(
                ref_text,
                font="Latin Modern Mono",
                font_size=self.FONT_SIZE_FOOTNOTE,
                color=self.get_color("highlight"),
            )
            footer_refs.add(footer_ref)

        # Organizando verticalmente com espaçamento
        footer_refs.arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # Posicionando na parte inferior do slide
        footer_refs.to_edge(DOWN).shift(UP * 0.3)

        return footer_refs
    '''

    def caption(self, figure, label):
        """
        Cria uma legenda numerada para figuras usando Tex para suporte a símbolos matemáticos.

        Args:
            figure: O objeto Manim que representa a figura
            label: O texto da legenda (pode conter LaTeX como $\\beta$, $\\alpha$, etc.)

        Returns:
            Tex: Objeto de texto com a legenda formatada

        Example:
            plot = self.create_some_plot()
            caption = self.caption(plot, r"Gráfico de $\beta$ vs $T_c$")
            self.add(plot, caption)
        """
        # Incrementa o contador global de figuras
        CustomSlide.current_figure += 1
        fig_num = CustomSlide.current_figure

        # Cria a legenda usando Tex para suporte a LaTeX.
        # Adicionamos um ponto final e o número da figura
        fig_caption = MathTex(
            f"\\text{{Fig. }}{fig_num}: {label}.",
            font_size=self.FONT_SIZE_CAPTION,
            color=self.get_color("text"),
        )

        # Posiciona a legenda abaixo da figura
        fig_caption.next_to(figure, DOWN, buff=0.2)

        return fig_caption

    def create_numbered_equation(self, tex_string, font_size=None):
        """
        Cria uma equação numerada automaticamente.

        Args:
            tex_string: String LaTeX para a equação OU lista de strings que serão concatenadas
            font_size: Tamanho da fonte
            latex_style: Se True, posiciona numeração estilo LaTeX (direita da tela)

        Returns:
            VGroup: Grupo contendo equação e numeração (se string única) OU
                    grupo contendo partes da equação e numeração (se lista de strings)

        Examples:
            # String única
            eq = self.create_numbered_equation("E = mc^2")

            # Lista de strings (para animações)
            eq = self.create_numbered_equation(["E", "=", "mc^2"])
            # Agora você pode acessar: eq[0] (primeira parte), eq[1] (segunda parte), etc.
        """
        # Incrementar contador de equações
        if not hasattr(self, "equation_counter"):
            self.equation_counter = 0
        self.equation_counter += 1

        # Criar equação
        if font_size is None:
            font_size = self.FONT_SIZE_EQ_TEXT

        # Inicializar tex_template se não existir
        if not hasattr(self, "tex_template"):
            from manim import TexTemplate

            self.tex_template = TexTemplate()
            self.tex_template.add_to_preamble(r"\usepackage{mathrsfs}")
            self.tex_template.add_to_preamble(r"\usepackage{amsmath}")
            self.tex_template.add_to_preamble(r"\usepackage{amssymb}")

        # Verificar se tex_string é uma lista ou string única
        if isinstance(tex_string, list):
            # Criar MathTex com lista de strings (permite acesso individual)
            equation = MathTex(
                *tex_string, font_size=font_size, tex_template=self.tex_template
            ).set_color(self.get_color("text"))
        else:
            # Criar MathTex com string única (comportamento original)
            equation = MathTex(
                tex_string, font_size=font_size, tex_template=self.tex_template
            ).set_color(self.get_color("text"))

        # Criar numeração
        number = MathTex(f"({self.equation_counter})", font_size=font_size).set_color(
            self.get_color("primary")
        )
        
        number.next_to(equation, RIGHT, buff=0.3)

        return VGroup(equation, number)

    def align_equation_numbers(self, equations_list):
        """
        Realinha os números das equações na margem direita após o posicionamento das equações.
        Use este método depois de posicionar as equações com .arrange() ou .move_to().

        Args:
            equations_list: Lista de objetos retornados por create_numbered_equation

        Example:
            eq1 = self.create_numbered_equation("E = mc^2")
            eq2 = self.create_numbered_equation("F = ma") 
            eq3 = self.create_numbered_equation("p = mv")
            
            equations = VGroup(eq1, eq2, eq3)
            equations.arrange(DOWN, buff=0.8).center()
            
            # Realinhar números após posicionamento
            self.align_equation_numbers([eq1, eq2, eq3])
        """
        for eq_group in equations_list:
            if len(eq_group) >= 2:  # Verifica se tem equação e número
                equation = eq_group[0]
                number = eq_group[1]
                
                # Reposiciona o número mantendo x fixo na margem direita
                current_x = number.get_x()  # Mantém posição X atual (margem direita)
                equation_y = equation.get_y()  # Pega nova posição Y da equação
                
                number.move_to([current_x, equation_y, 0])

    def create_equation_numbers_group(self, equations_list):
        """
        Cria um grupo separado apenas com as numerações das equações.
        Útil para posicionamento manual independente.

        Args:
            equations_list: Lista de objetos retornados por create_numbered_equation

        Returns:
            VGroup: Grupo contendo apenas as numerações

        Example:
            eq1 = self.create_numbered_equation("E = mc^2")
            eq2 = self.create_numbered_equation("F = ma")

            # Criar grupo independente das numerações
            numbers_group = self.create_equation_numbers_group([eq1, eq2])
            numbers_group.arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=0.3)
        """
        numbers = [eq[-1] for eq in equations_list]
        return VGroup(*numbers)


class PlotBase:
    """
    Base class for creating scientific diagrams with consistent styling and common functionality.

    This class provides the foundation for all diagram types, including axes creation,
    styling, labeling, and common plot elements. Specific diagram types inherit from
    this class and implement their own data visualization logic.

    Design Philosophy:
        - Single Responsibility: Base class handles universal diagram elements
        - Consistent Styling: All derived diagrams share the same visual language
        - Extensibility: Easy to create new diagram types by inheritance
        - Manim-Native: Returns standard VGroup objects for seamless integration

    Attributes:
        custom_slide: Reference to the parent slide object for style consistency
        data_path (str): Path to the directory containing data files
        x_range (list): Range for the x-axis [min, max, step]
        y_range (list): Range for the y-axis [min, max, step]
        x_length (float): Physical length of the x-axis
        y_length (float): Physical length of the y-axis
        x_label (str): Label for the x-axis
        y_label (str): Label for the y-axis
        axes (Axes): Manim Axes object for coordinate calculations (internal use only)
        diagram_group (VGroup): Group containing all visual elements of the diagram
    """

    def __init__(
        self,
        custom_slide,
        data_path="plots/",
        x_range=[0, 1.0, 0.2],
        y_range=[0, 4.0, 1],
        x_length=5,
        y_length=3.75,
        x_label="x",
        y_label="y",
    ):
        """
        Initialize the base plot with common parameters.

        Args:
            custom_slide: Reference to the parent slide for style consistency
            data_path: Path to data files directory
            x_range: Range for x-axis [min, max, step]
            y_range: Range for y-axis [min, max, step]
            x_length: Physical length of x-axis in Manim units
            y_length: Physical length of y-axis in Manim units
            x_label: Label text for x-axis
            y_label: Label text for y-axis
        """
        self.custom_slide = custom_slide
        self.data_path = data_path
        self.x_range = x_range
        self.y_range = y_range
        self.x_length = x_length
        self.y_length = y_length
        self.x_label = x_label
        self.y_label = y_label

        # Will be created by subclasses
        self.axes = None
        self.diagram_group = None

    def _create_axes(self):
        """Create the base axes system"""
        self.axes = Axes(
            x_range=self.x_range,
            y_range=self.y_range,
            x_length=self.x_length,
            y_length=self.y_length,
            axis_config={
                "color": self.custom_slide.get_color("text"),
                "include_tip": False,
                "stroke_width": 2,
            },
            tips=False,
        )
        return self.axes

    def _create_plot_area(self):
        """Create the rectangular border around the plot"""
        bottom_left = self.axes.coords_to_point(self.x_range[0], self.y_range[0])
        top_right = self.axes.coords_to_point(self.x_range[1], self.y_range[1])

        plot_width = top_right[0] - bottom_left[0]
        plot_height = top_right[1] - bottom_left[1]

        plot_area = Rectangle(
            width=plot_width,
            height=plot_height,
            color=self.custom_slide.get_color("text"),
            fill_opacity=0,
            stroke_width=2,
        )

        plot_center_x = (bottom_left[0] + top_right[0]) / 2
        plot_center_y = (bottom_left[1] + top_right[1]) / 2
        plot_area.move_to([plot_center_x, plot_center_y, 0])

        return plot_area

    def _create_ticks(self, x_ticks=None, y_ticks=None):
        """
        Create tick marks and labels

        Args:
            x_ticks: List of x-axis tick positions. If None, uses default spacing
            y_ticks: List of y-axis tick positions. If None, uses default spacing
        """
        x_tick_group = VGroup()
        y_tick_group = VGroup()
        x_tick_labels = VGroup()
        y_tick_labels = VGroup()

        # Default tick positions if not specified
        if x_ticks is None:
            x_step = self.x_range[2]
            x_ticks = [i * x_step for i in range(int(self.x_range[1] / x_step) + 1)]

        if y_ticks is None:
            y_step = self.y_range[2]
            y_ticks = [i * y_step for i in range(int(self.y_range[1] / y_step) + 1)]

        # X-axis ticks
        for x_val in x_ticks:
            if self.x_range[0] <= x_val <= self.x_range[1]:
                tick_pos = self.axes.coords_to_point(x_val, self.y_range[0])
                tick = Line(
                    tick_pos + 0.05 * DOWN,
                    tick_pos + 0.05 * UP,
                    color=self.custom_slide.get_color("text"),
                    stroke_width=2,
                )
                x_tick_group.add(tick)

                # Format number to remove unnecessary decimal places
                if x_val == int(x_val):
                    label_text = str(int(x_val))
                else:
                    label_text = f"{x_val:.1f}"

                label = Text(
                    label_text, font_size=18, color=self.custom_slide.get_color("text")
                )
                label.next_to(tick, DOWN, buff=0.1)
                x_tick_labels.add(label)

        # Y-axis ticks
        for y_val in y_ticks:
            if self.y_range[0] <= y_val <= self.y_range[1]:
                tick_pos = self.axes.coords_to_point(self.x_range[0], y_val)
                tick = Line(
                    tick_pos + 0.05 * LEFT,
                    tick_pos + 0.05 * RIGHT,
                    color=self.custom_slide.get_color("text"),
                    stroke_width=2,
                )
                y_tick_group.add(tick)

                # Format number to remove unnecessary decimal places
                if y_val == int(y_val):
                    label_text = str(int(y_val))
                else:
                    label_text = f"{y_val:.1f}"

                label = Text(
                    label_text, font_size=18, color=self.custom_slide.get_color("text")
                )
                label.next_to(tick, LEFT, buff=0.1)
                y_tick_labels.add(label)

        return x_tick_group, y_tick_group, x_tick_labels, y_tick_labels

    def _create_axis_labels(self):
        """Create axis labels"""
        plot_area = self._create_plot_area()  # Temporary for positioning

        x_label = MathTex(
            self.x_label,
            font_size=30,
            color=self.custom_slide.get_color("series4", "graph"),
        )
        x_label.next_to(plot_area, DOWN, buff=0.5)

        y_label = MathTex(
            self.y_label,
            font_size=30,
            color=self.custom_slide.get_color("series4", "graph"),
        )
        y_label.next_to(plot_area, LEFT, buff=0.5)

        return x_label, y_label

    def _load_data(self, filename, data_path=None, fallback_data=None, comments="#"):
        """
        Load data from a file with error handling and fallback.

        This universal data loading method provides consistent error handling,
        fallback data support, and flexible path configuration for all diagram types.

        Args:
            filename (str): Name of the data file to load
            data_path (str, optional): Path to the data directory. If None, uses self.data_path
            fallback_data (ndarray, optional): Fallback data to use if file loading fails
            comments (str, optional): Character used to indicate comments. Default: "#"

        Returns:
            ndarray: Loaded data from file or fallback data

        Raises:
            FileNotFoundError: If file not found and no fallback data provided
            ValueError: If data format is invalid and no fallback data provided

        Example:
            # Basic usage with default data path
            af_saf_data = self._load_data("Transition--AF-SAF.dat")

            # With custom path and fallback
            custom_data = self._load_data(
                "custom_file.dat",
                data_path="custom_path/",
                fallback_data=np.array([[0, 1], [1, 2]])
            )
        """
        # Use provided data_path or default to instance data_path
        if data_path is None:
            if hasattr(self, "data_path"):
                data_path = self.data_path
            else:
                data_path = ""

        # Construct full file path
        file_path = data_path + filename

        try:
            # Attempt to load data from file
            data = np.loadtxt(file_path, comments=comments)
            return data

        except FileNotFoundError as e:
            print(f"Warning: Data file '{file_path}' not found.")
            if fallback_data is not None:
                print(f"Using fallback data for '{filename}'")
                return fallback_data
            else:
                print(f"No fallback data provided for '{filename}'")
                raise FileNotFoundError(
                    f"Data file '{file_path}' not found and no fallback provided"
                ) from e

        except Exception as e:
            print(f"Error loading data from '{file_path}': {e}")
            if fallback_data is not None:
                print(f"Using fallback data for '{filename}'")
                return fallback_data
            else:
                print(f"No fallback data provided for '{filename}'")
                raise ValueError(
                    f"Invalid data format in '{file_path}' and no fallback provided"
                ) from e

    def get_mobject(self):
        """
        Return the complete diagram as a Manim VGroup object.

        This method should be implemented by subclasses to return their
        specific diagram structure.
        """
        if self.diagram_group is None:
            raise NotImplementedError("Subclasses must implement diagram creation")
        return self.diagram_group

    def get_axes(self):
        """Return the axes object for advanced coordinate calculations"""
        return self.axes


class CustomMovingCameraSlide(CustomSlide, MovingCameraScene):
    """Classe que combina CustomSlide com MovingCameraScene para movimento de câmera"""

    def __init__(self, *args, **kwargs):
        # Chama o __init__ do CustomSlide para configurar cores, fontes, etc.
        super().__init__(*args, **kwargs)

        # MovingCameraScene já é inicializada pela herança múltipla
        # Aqui podemos fazer configurações específicas da câmera se necessário
