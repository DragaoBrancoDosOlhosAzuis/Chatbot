from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionDeterminarAjuda(Action):
    def name(self) -> Text:
        return "action_determinar_ajuda"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        problema = tracker.get_slot("problema")
        if problema:
            if problema == "acesso":
                dispatcher.utter_message(response="utter_resposta_acesso")
            elif problema == "mudar_plano":
                dispatcher.utter_message(response="utter_resposta_mudar_plano")
            elif problema == "problema_tecnico":
                dispatcher.utter_message(response="utter_resposta_tecnico")
        else:
            dispatcher.utter_message(response="utter_nao_entendi")
        
        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_nao_entendi")
        return []