from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests

class ActionBuscarLivroTitulo(Action):
    def name(self) -> Text:
        return "action_buscar_livro_titulo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        titulo = tracker.get_slot("titulo_livro") or next(tracker.get_latest_entity_values("titulo_livro"), None)
        
        if not titulo:
            dispatcher.utter_message(text="Não consegui identificar o título do livro. Poderia repetir?")
            return []
        
        url = f"https://openlibrary.org/search.json?title={titulo}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            books = data.get("docs", [])[:5]
            
            if not books:
                return [SlotSet("livro_encontrado", None)]
            
            results = []
            for book in books:
                title = book.get("title", "Título desconhecido")
                author = book.get("author_name", ["Autor desconhecido"])[0]
                year = book.get("first_publish_year", "Ano desconhecido")
                results.append(f"'{title}' por {author} ({year})")
            
            return [SlotSet("livro_encontrado", results)]
        else:
            return [SlotSet("livro_encontrado", None)]

class ActionBuscarLivroAutor(Action):
    def name(self) -> Text:
        return "action_buscar_livro_autor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        autor = tracker.get_slot("nome_autor") or next(tracker.get_latest_entity_values("nome_autor"), None)
        
        if not autor:
            dispatcher.utter_message(text="Não consegui identificar o nome do autor. Poderia repetir?")
            return []
        
        url = f"https://openlibrary.org/search.json?author={autor}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            books = data.get("docs", [])[:5]
            
            if not books:
                return [SlotSet("autor_encontrado", None)]
            
            results = []
            for book in books:
                title = book.get("title", "Título desconhecido")
                author = book.get("author_name", ["Autor desconhecido"])[0]
                year = book.get("first_publish_year", "Ano desconhecido")
                results.append(f"'{title}' por {author} ({year})")
            
            return [SlotSet("autor_encontrado", results)]
        else:
            return [SlotSet("autor_encontrado", None)]

class ActionBuscarLivroAssunto(Action):
    def name(self) -> Text:
        return "action_buscar_livro_assunto"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        assunto = tracker.get_slot("assunto_livro") or next(tracker.get_latest_entity_values("assunto_livro"), None)
        
        if not assunto:
            dispatcher.utter_message(text="Não consegui identificar o assunto. Poderia repetir?")
            return []
        
        url = f"https://openlibrary.org/search.json?q={assunto}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            books = data.get("docs", [])[:5]
            
            if not books:
                return [SlotSet("assunto_encontrado", None)]
            
            results = []
            for book in books:
                title = book.get("title", "Título desconhecido")
                author = book.get("author_name", ["Autor desconhecido"])[0]
                subject = book.get("subject", ["Assunto desconhecido"])[0]
                results.append(f"'{title}' por {author} (sobre {subject})")
            
            return [SlotSet("assunto_encontrado", results)]
        else:
            return [SlotSet("assunto_encontrado", None)]

class ActionMostrarResultados(Action):
    def name(self) -> Text:
        return "action_mostrar_resultados"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        livro_encontrado = tracker.get_slot("livro_encontrado")
        autor_encontrado = tracker.get_slot("autor_encontrado")
        assunto_encontrado = tracker.get_slot("assunto_encontrado")
        
        if livro_encontrado:
            dispatcher.utter_message(text="Aqui estão alguns livros que encontrei com esse título:")
            for book in livro_encontrado:
                dispatcher.utter_message(text=book)
            return [SlotSet("livro_encontrado", None)]
        
        elif autor_encontrado:
            dispatcher.utter_message(text="Aqui estão alguns livros desse autor:")
            for book in autor_encontrado:
                dispatcher.utter_message(text=book)
            return [SlotSet("autor_encontrado", None)]
        
        elif assunto_encontrado:
            dispatcher.utter_message(text="Aqui estão alguns livros sobre esse assunto:")
            for book in assunto_encontrado:
                dispatcher.utter_message(text=book)
            return [SlotSet("assunto_encontrado", None)]
        
        else:
            dispatcher.utter_message(text="Não encontrei resultados para essa busca.")
            return []