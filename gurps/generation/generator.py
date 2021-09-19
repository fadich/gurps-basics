from random import choice, randint
from typing import Sequence, Optional

from gurps import roll

from gurps.character import (
    Character,
    Feature,
    Skill,
    features,
    skills,
)


class CharacterGenerator:
    NAMES = [
        'Ренди (М)',
        'Джонатан (М)',
        'Арни (М)',
        'Игри (Ж)',
        'Терра (Ж)',
        'Элин (Ж)',
        'Стур (М)',
        'Жорд (М)',
        'Арни (М)',
        'Арни (Ж)',
        'Дженни (Ж)',
        'Дженнифер (Ж)',
        'Стардар (М)',
        'Арго (М)',
        'Мира (Ж)',
        'Загра (Ж)',
        'Зурмаль (М)',
        'Эрика (Ж)',
    ]
    APPEARANCE = [
        'шрам на лице',
        'ожоги на лице',
        'ожоги на руках',
        'татуировка на лице',
        'татуировка на руке (или где-то еще)',
        'редкие волосы',
        'веснушки',
        'очень длинные волосы (коса)',
        'очень длинные волосы (распущенные)',
        'храмает (на левую ногу)',
        'нет руки (DX/2)',
        'нет левого уха',
        'нет пальца',
        'голубые глаза',
        'зеленые глаза',
        'седые волосы',
        'нет глаза',
        'лысый(-ая)',
        'лысый(-ая), татуировка на голове',
        'прячет лицо',
        'нет ноги (DX/2)',
        'горб',
        'идет, будто пишет',
        'темнокожий',
        'альбинос',
        'седой',
        'молодой',
        'пожилой',
        'молодой, но седой',
    ]
    BEHAVIOURS = [
        'спокойный',
        'угрюмый',
        'разговорчивый',
        'молчаливый',
        'добрый',
        'готов помочь',
        'одиночка',
        'эгоист',
        'законопослушный',
        'суетливый',
        'дерзкий',
        'шутник',
        'застенчивый',
        'скрытный',
        'молчаливый',
        'доверчивый',
    ]
    ITEMS = [
        'роба',
        'роба',
        'роба',
        'балахон',
        'балахон',
        'латы (PD: 6 // DR: 6)',
        'полулаты (PD: 4 // DR: 4)',
        'кольчуга (PD: 3 (1 против кол.) // DR: 4 (2 против кол.))',
        'кожаный доспех (PD: 2 // DR: 2)',
        'кожаный доспех (PD: 2 // DR: 2)',
        'кожаный доспех (PD: 2 // DR: 2)',
        'легкая одежда (PD: 0 // DR: 0)',
        'легкая одежда (PD: 0 // DR: 0)',
        'легкая одежда (PD: 0 // DR: 0)',
        'плотная одежда (PD: 1 // DR: 1)',
        'плотная одежда (PD: 1 // DR: 1)',
        f'посох ({randint(13, 18)}) - 1к',
        f'короткий меч ({randint(13, 18)}) - 1к+2 руб./ 1к-1 кол.',
        f'двуручный меч ({randint(13, 18)}) - 2к руб./ 1к+1 кол.',
        f'дубина ({randint(13, 18)}) - 1к+1',
        f'топор ({randint(13, 18)}) - 1к+2',
        f'секира ({randint(13, 18)}) - 2к+2',
        f'копье ({randint(13, 18)}) 1к+2',
        f'2 ножа ({randint(13, 18)}) - 1к-1',
        f'лук ({randint(13, 18)}) - 1к',
        f'арбалет ({randint(13, 18)}) - 1к+2',
        'большой рюкзак',
        'большой мешок (нагрузка +1)',
        '2 больших мешока (нагрузка +2)',
        f'малый щит ({randint(13, 18)}) - +2PD',
        f'большой щит ({randint(13, 18)}) - +4PD',
    ]

    def __init__(
        self,
        max_appearance: Optional[int] = None,
        max_items: Optional[int] = None,
        max_behaviors: Optional[int] = None,
        max_features: Optional[int] = None,
        max_skills: Optional[int] = None
    ):
        self.max_appearance = max_appearance
        self.max_items = max_items
        self.max_behaviors = max_behaviors
        self.max_features = max_features
        self.max_skills = max_skills

    def generate(self):
        return Character(
            name=self._generate_name(),
            st=self._generate_attribute(),
            dx=self._generate_attribute(),
            iq=self._generate_attribute(),
            ht=self._generate_attribute(),
            features=self._generate_features(
                advantages=1,
                disadvantages=1
            ),
            skills=self._generate_skills(),
            notes=self._generate_notes()
        )

    def _generate_name(self):
        return choice(self.NAMES)

    def _generate_notes(self):
        appearance = []
        items = []
        behaviors = []

        for _ in range(int(roll('3d6') / 6)):
            appearance.append(
                choice(self.APPEARANCE)
            )

        for _ in range(int(roll('3d6') / 4)):
            behaviors.append(
                choice(self.BEHAVIOURS)
            )

        for _ in range(int(roll('3d6') / 4)):
            items.append(
                choice(self.ITEMS)
            )

        if self.max_appearance is not None:
            appearance = appearance[:self.max_appearance]

        if self.max_items is not None:
            items = appearance[:self.max_items]

        if self.max_behaviors is not None:
            behaviors = appearance[:self.max_behaviors]

        return '\n\t'.join([
            "; ".join(appearance).capitalize(),
            "; ".join(items).capitalize(),
            "; ".join(behaviors).capitalize(),
        ])

    def _generate_attribute(self, bonus: int = 0):
        return roll(f'3d6+{bonus}')

    def _generate_features(
        self,
        advantages: int = 1,
        disadvantages: int = 1,
        quirks: int = 0
    ):
        ftrs = []

        for _ in range(advantages):
            ftrs.extend(self._generate_advantages())

        for _ in range(disadvantages):
            ftrs.extend(self._generate_disadvantages())

        for _ in range(quirks):
            ftrs.extend(self._generate_quirks())

        ftrs = tuple({  # Filter unique values
            f.__class__: f for f in ftrs
        }.values())

        if self.max_features is not None:
            ftrs = ftrs[:self.max_features]

        return ftrs

    def _generate_advantages(self) -> Sequence[Feature]:
        res = roll('3d6')

        if res in (3, 17, 18):
            return [
                *self._generate_advantages(),
                *self._generate_advantages(),
            ]

        feature = {
            4: features.Voice(),
            5: features.Charisma(level=6),
            6: features.Alertness(level=4),
            7: features.CommonSense(),
            8: features.Magery(level=2),
            9: features.AcuteVision(level=5),
            10: features.Alertness(level=2),
            11: features.Charisma(level=3),
            12: features.AcuteTasteAndSmell(level=5),
            13: features.DangerSense(),
            14: features.Appearance(level=1),
            15: features.AcuteHearing(level=5),
            16: features.Appearance(level=2),
        }[res]

        return [feature, ]

    def _generate_disadvantages(self) -> Sequence[Feature]:
        res = roll('3d6')

        if res in (3, 17, 18):
            return [
                *self._generate_advantages(),
                *self._generate_advantages(),
            ]

        poverty = Feature(  # TODO: Create Feature "Богатство"
            name='Бедность (Poverty)',
            description='-2 к реакции',
            cost=-15
        )
        habit = choice([
            'курит',
            'харкает',
            'жует табак',
            'ковыряет в носу',
            'ковыряет в ухе',
            'отрыгивает',
            'громко пукает',
            'выпивает',
            'что-то жует, ест',
            'матерится',
            'грызет ногти',
            'употребляет наркотики',
        ])
        bad_habit = Feature(
            name=f'Вредная привычка: {habit} (-2 к реакции)',
            description='-2 к реакции',
            cost=-10
        )

        feature = {
            4: poverty,
            5: features.Cowardice(),
            6: bad_habit,
            7: bad_habit,
            8: features.BadTemper(),
            9: features.Unluckiness(),
            10: features.Greed(),
            11: features.Overconfidence(),
            12: features.Honesty(),
            13: features.HardOfHearing(),
            14: features.Appearance(level=-1),
            15: features.BadSight(),
            16: features.Appearance(level=-3),
        }[res]

        return [feature, ]

    def _generate_quirks(self) -> Sequence[Feature]:
        return []

    def _generate_skills(self) -> Sequence[Skill]:
        skls = []

        # TODO: Fix this mocking - use real skills
        names = {
            3: ('Каллиграфия', 'Оружейное дело', 'Биохимия'),
            4: ('Ботаника', 'Торговое дело', 'Ловкость рук'),
            5: ('Дипломатия', 'Врачебное дело', 'Спорт (любой)'),
            6: ('Пение', 'Язык (любой)', 'Ветеринария'),
            7: ('Приручение животных', 'Бард', 'Артистизм'),
            8: (
                'Тихое передвижение',
                'Собирание (Scrounging)',
                'Первая помощь'
            ),
            9: (
                'Холодное оружие (любое)',
                'Быстрая подготовка оружия (любого)',
                'Лазание'
            ),
            10: ('Холодное оружие (любое)', 'Ловушки', 'Владение щитом'),
            11: (
                'Бег (перемещение +1)',
                'Драка',
                'Вождение или Верховая езда (любая)'
            ),
            12: (
                'Оружие дальнего боя',
                'Пилотирование или Тяжелое оружие (любое)',
                'Плавание'
            ),
            13: ('Пирушки', 'Законы', 'Хорошие манеры'),
            14: ('Азартные игры', 'Знание улиц', 'Политика'),
            15: (
                'Музыкальный инструмент (любой)',
                'Выживание(любое)',
                'Взлом'
            ),
            16: ('Подделка', 'Маскировка', 'Механика'),
            17: ('Дзюдо или Карате', 'Натуралист', 'Сексапильность'),
            18: ('История', 'Навигация', 'Яды'),
        }

        for i in range(int(roll('3d6') / 2)):
            skill = Skill(
                name=names[roll('3d6')][randint(0, 2)],
                description='',
                based_on_name='',
                based_on_reference=10
            )
            skill.level = 12 + roll('1d6')
            skls.append(skill)

        skls = tuple({  # Filter unique values
             hash(s): s for s in skls
         }.values())

        if self.max_skills is not None:
            skls = skls[:self.max_skills]

        return sorted(skls, key=lambda s: s.level, reverse=True)


if __name__ == '__main__':
    for _ in range(10):
        print('=' * 120)
        print(
            CharacterGenerator().generate()
        )

    print('=' * 120)
