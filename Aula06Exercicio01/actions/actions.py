import requests  # Biblioteca para fazer requisições HTTP
from typing import Any, Text, Dict, List  # Tipagem para facilitar a leitura do código
from rasa_sdk import Action, Tracker  # Importação de classes para criar a custom action
from rasa_sdk.executor import CollectingDispatcher  # Classe que permite enviar respostas ao usuário

class ActionInformaClima(Action):
    def name(self) -> Text:
        """
        Define o nome da action. Esse nome deve ser o mesmo registrado no domain.yml.
        """
        return "action_informa_clima"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Este método é chamado quando a action é executada. Ele:
        - Obtém a cidade da mensagem do usuário
        - Consulta a API de clima
        - Envia a resposta ao usuário
        """
        # Captura o nome da cidade a partir da mensagem mais recente do usuário
        city = tracker.latest_message['text']

        # Chama a API para obter os dados do clima
        weather_data = self.get_weather(city)

        print(f"City: {city}")
        print(f"Weather Data: {weather_data}")

        if weather_data:
            # Se os dados forem recebidos, formata a resposta com a temperatura
            response = f"O clima na cidade de {city} está em: {weather_data['current']['temp_c']} °C."
        else:
            # Se não conseguir buscar os dados, informa o erro
            response = f"Me desculpe, mas não consegui obter a situação do clima da cidade de {city}."

        # Envia a resposta ao usuário
        dispatcher.utter_message(text=response)
        return []

    @staticmethod
    def get_weather(city: str) -> Dict[Text, Any]:
        """
        Método responsável por consultar a API de clima e retornar os dados.
        """
        api_key = "989cb01b25534744a08225015252503"  # Chave da API (substitua pela sua!)
        base_url = "http://api.weatherapi.com/v1/current.json"
        params = {
            "q": city,  # Parâmetro da cidade a ser consultada
            "aqi": "no",  # Não incluir dados de qualidade do ar
            "key": api_key  # Chave de acesso à API
        }

        try:
            # Faz a requisição GET para a API
            print(f"API Request URL: {base_url}?{params}")
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Verifica se houve erro na requisição
            api_response = response.json()  # Converte a resposta para JSON
            print(f"API Response: {api_response}")
            return api_response
        except requests.exceptions.RequestException as e:
            # Captura erros na requisição e imprime no console
            print(f"API Request Error: {e}")
        return None