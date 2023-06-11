class SURVEY:
    def survey_yes_no(self):
        survey_data = {
        'question' : 'Двигатель запускается?',
        'answer' : ['Запускается', 'Не запускается']
        }
        return survey_data

    
    def survey_yes_1(self):
        survey_data = {
        'question' : 'Двигатель работает устойчиво? (стрелка тахометра стоит ровно и показывает около 700-800 оборотов)',
        'answer' : ['Устойчиво', 'Не устойчиво']
        }
        return survey_data


    def survey_yes_2(self):
        survey_data = {
        'question' : 'На холостом ходу двигатель развивает слишком высокие обороты?',
        'answer' : ['Да', 'Нет']
        }
        return survey_data


    def survey_yes_3(self):
        survey_data = {
        'question' : 'При движении ощущается пониженная мощность и приемистость двигателя?',
        'answer' : ['Ощущается', 'Не ощущается']
        }
        return survey_data


    def survey_no_1(self):
        survey_data = {
        'question' : 'Стартер крутит? (соответствующий звук из-под капота, после проворта ключа в замке зажигания)',
        'answer' : ['Крутит', 'Не крутит']
        }
        return survey_data


    def survey_no_2(self):
        survey_data = {
        'question' : 'Стартер крутит хорошо или плохо? (плохо - характерный шуршащий звук)',
        'answer' : ['Хорошо', 'Плохо']
        }
        return survey_data


    def survey_no_3(self):
        survey_data = {
        'question' : 'При включении зажигания имеется ли характерный звук жужжания в салоне?',
        'answer' : ['Имеется', 'Не имеется']
        }
        return survey_data