# Apresentação Unificada - Seminário sobre Expoentes Críticos
# Integra todos os slides individuais em uma apresentação única
# M. Roos, 20/06/2025

from manim import *
from manim_slides import Slide
from components.custom_slide import CustomSlide

# Importar todos os slides
from slides.cover import Cover
from slides.overview import Overview
from slides.slide3 import Slide3
from slides.slide4 import Slide4
from slides.slide5 import Slide5
from slides.slide6 import Slide6
from slides.slide7 import Slide7
from slides.slide8 import Slide8


class FullPresentation(CustomSlide):
    """
    Apresentação completa que integra todos os slides individuais
    em uma sequência unificada com configurações consistentes.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skip_reversing = True  # Desabilita reversão automática
        self.slide_count = 0
        
        # Configurar template LaTeX global para toda a apresentação
        self.setup_global_tex_template()
        
    def setup_global_tex_template(self):
        """
        Configura um template LaTeX global para toda a apresentação
        com pacotes necessários como mathrsfs
        """
        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
        # Adicione outros pacotes conforme necessário
        # self.myTemplate.add_to_preamble(r"\usepackage{amsmath}")
        # self.myTemplate.add_to_preamble(r"\usepackage{amssymb}")
        
        # Tornar o template disponível para todos os slides filhos
        CustomSlide.global_tex_template = self.myTemplate
        
    def construct(self):        
        # Executar slides em sequência
        self.run_cover_slide() # Slide 0: Cover (sem numeração)
        self.setup_scene()         # Numera o slide
        self.run_overview()               # Slide 2: Overview
        self.run_slide3() # Slide 3: Introduction
        self.run_slide4() # Slide 4: Campo Médio no Ising
        self.run_slide5() # Slide 5: Teoria de Landau e Resultados analíticos e experimentais
        self.run_slide6() # Slide 6: Funções Homogêneas e hipóteses de escala
        self.run_slide7() # Slide 7: Finite-size scaling
        self.run_slide8() # Slide 8: Conclusão
        
        
        # Slide final de agradecimentos
        #self.run_final_slide()
    
    def setup_global_presentation(self):
        """
        Configura elementos globais da apresentação que devem ser consistentes
        em todos os slides (numeração, etc.)
        """
        # Configurar a cena base uma única vez
        self.setup_scene()
        
    def clear_scene_for_next_slide(self):
        """
        Limpa a cena para o próximo slide, mantendo apenas elementos globais
        como numeração de slides.
        """
        # Remove todos os objetos exceto os elementos da base
        mobjects_to_remove = []
        
        for mob in self.mobjects:
            # Manter elementos da timeline
            should_preserve = False
            
            # Verificar se é o slide number (armazenado no canvas)
            if hasattr(self, 'canvas') and 'slide_number' in self.canvas and mob == self.canvas['slide_number']:
                should_preserve = True
            
            # Verificar se é parte da timeline usando a lista de objetos
            if hasattr(self, 'timeline_objects') and mob in self.timeline_objects:
                should_preserve = True
            
            # Se não deve ser preservado, adicionar à lista de remoção
            if not should_preserve:
                mobjects_to_remove.append(mob)
        
        if mobjects_to_remove:
            self.remove(*mobjects_to_remove)
    
    def transition_to_next_slide(self):
        """
        Executa uma transição suave entre slides com mensagem opcional.
        """
        # A cada novo slide, incrementa o contador de páginas
        self.next_slide(update_number=True)
        
        # Opcional. Se ativado, adicionar esse arg:
        # message=None
        #if message:
        #    transition_text = Text(
        #        message,
        #        font_size=self.FONT_SIZE_TEXT,
        #        color=self.get_color("emphasis")
        #    )
        #    transition_text.center()
        #    self.play(FadeIn(transition_text), run_time=0.5)
        #    self.wait(0.5)
        #    self.play(FadeOut(transition_text), run_time=0.5)
        
        self.clear_scene_for_next_slide()
    
    def run_cover_slide(self):
        """Executa o slide de capa."""
        print("Executando slide: Cover")
        
        # Criar instância do slide de capa
        cover_slide = Cover()
        
        # Configurar o slide para usar o mesmo renderer/camera
        cover_slide.renderer = self.renderer
        
        # Usar o método mais seguro: salvar mobjects atuais e restaurar depois
        original_mobjects = self.mobjects.copy()
        
        # Limpar mobjects para o slide de capa (mantendo timeline)
        #timeline_mobjects = []
        #if hasattr(self, 'timeline_group'):
        #    timeline_mobjects = list(self.timeline_group)
        #    
        #self.mobjects = timeline_mobjects.copy()
        
        # Executar o construct do slide, mas redirecionando operações para esta cena
        self._execute_slide_construct(cover_slide)
        self.next_slide()
        self.clear_scene_for_next_slide()

    def run_overview(self):
        """Running overview."""
        print("Executando slide: Overview")
        
        overview_slide = Overview()
        self._execute_slide_construct(overview_slide)
        self.transition_to_next_slide()
    
    def _execute_slide_construct(self, slide_instance):
        """
        Executa o construct de um slide redirecionando as operações para esta cena.
        """
        # Salvar métodos originais
        original_play = slide_instance.play
        original_add = slide_instance.add
        original_remove = slide_instance.remove
        original_wait = slide_instance.wait
        original_next_slide = slide_instance.next_slide
        original_setup_scene = getattr(slide_instance, 'setup_scene', None)
        #original_setup_timeline = getattr(slide_instance, 'setup_timeline', None)
        
        # Redirecionar métodos para esta cena
        slide_instance.play = self.play
        slide_instance.add = self.add
        slide_instance.remove = self.remove
        slide_instance.wait = self.wait
        slide_instance.next_slide = self.next_slide
        
        # Desabilitar setup_scene e setup_timeline nos slides individuais
        # para evitar duplicação de elementos globais
        slide_instance.setup_scene = lambda: None
        #slide_instance.setup_timeline = lambda: None
        
        # Copiar atributos de configuração
        #if hasattr(self, 'timeline_objects'):
        #    slide_instance.timeline_objects = self.timeline_objects
        #if hasattr(self, 'timeline'):
        #    slide_instance.timeline = self.timeline
        if hasattr(self, 'slide_counter'):
            slide_instance.slide_counter = self.slide_counter
        
        # Copiar métodos de tema/cores se existirem
        if hasattr(self, 'get_color'):
            slide_instance.get_color = self.get_color
        #if hasattr(self, 'setup_timeline'):
        #    slide_instance.setup_timeline = self.setup_timeline
        #if hasattr(self, 'highlight_timeline_event'):
        #    slide_instance.highlight_timeline_event = self.highlight_timeline_event
        
        try:
            # Executar o construct do slide
            slide_instance.construct()
        finally:
            # Restaurar métodos originais
            slide_instance.play = original_play
            slide_instance.add = original_add
            slide_instance.remove = original_remove
            slide_instance.wait = original_wait
            slide_instance.next_slide = original_next_slide
            if original_setup_scene:
                slide_instance.setup_scene = original_setup_scene
            #if original_setup_timeline:
            #    slide_instance.setup_timeline = original_setup_timeline
    
    
    def run_slide3(self):
        """Running Slide 3 - introduction."""
        print("Executando slide: Slide 3 - introduction")
        
        slide3 = Slide3()
        self._execute_slide_construct(slide3)
        self.transition_to_next_slide()
    
    def run_slide4(self):
        """Running Slide 4 - J1-J2-Jp Ising model on the BSL."""
        print("Executando slide: Slide 4 - J1-J2-Jp Ising model on the BSL")
        
        slide4 = Slide4()
        self._execute_slide_construct(slide4)
        self.transition_to_next_slide()
    
    def run_slide5(self):
        """Running Slide 5 - J1-Jx-Jp Ising model on the BSL."""
        print("Executando slide: Slide 5 - J1-Jx-Jp Ising model on the BSL")
        
        slide5 = Slide5()
        self._execute_slide_construct(slide5)
        self.transition_to_next_slide()

    def run_slide6(self):
        """Running Slide 6 - Quantum version."""
        print("Executando slide: Slide 6 - Quantum version")
        
        # Criar instância do slide de funções homogêneas
        slide6 = Slide6()
        self._execute_slide_construct(slide6)
        self.transition_to_next_slide()

    def run_slide7(self):
        """Running Slide 7 - Magnetic field case."""
        print("Executando slide 7 - Magnetic field case")

        slide7 = Slide7()
        self._execute_slide_construct(slide7)
        self.transition_to_next_slide()

    def run_slide8(self):
        """Running Slide 8 - Conclusion."""
        print("Executando slide 8 - Conclusion")

        slide8 = Slide8()
        self._execute_slide_construct(slide8)
        self.transition_to_next_slide()
    
    def run_final_slide(self):
        """Slide final de agradecimentos."""
        print("Executando slide final: Agradecimentos")
        
        # Black background (The End like movies)
        black_background = Square(color=BLACK, fill_opacity=1).scale(10)
        
        # Animações finais
        self.play(
            FadeIn(black_background),
            run_time=0.5
        )
        self.wait(0.5)
        
        capes_logo = ImageMobject("assets/logo_capes.png").scale(1)
        saia_logo = ImageMobject("assets/logo_SAIA.png").scale(2.5)
        logos = Group(capes_logo, saia_logo).arrange(DOWN, buff=1, aligned_edge=ORIGIN)
        self.play(
            FadeIn(logos, lag_ratio=0.5),
            run_time=1.0
        )
        self.wait()


# Classe auxiliar para testes individuais
class PresentationTest(FullPresentation):
    """
    Classe para testar partes específicas da apresentação.
    Útil para debug de slides individuais na apresentação unificada.
    """
    
    def construct(self):
        # Para testes, vamos seguir a mesma lógica da apresentação principal
        # mas executando apenas um slide por vez
        
        # Descomente o slide que quer testar:
        self.run_cover_slide()
        self.setup_scene()         # Numera o slide
        self.run_overview()
        self.run_slide3()
        self.run_slide4()
        self.run_slide5()
        self.run_slide6()
        self.run_slide7()
        self.run_slide8()
        self.run_final_slide()
