# SummarizerApp
## Обзор
Приложение использует предобученную языковую модель для обработки введённого текста (вручную или загруженного как `.txt` файл) и создания связного саммари, отражающего суть материала. Оно рассчитано на тексты разной длины — от коротких статей (~500 слов) до длинных документов (до 5000+ слов). Модель работает с английскими текстами.

## Требования
Python 3.8+

Необходимые библиотеки (см. requirements.txt)

## Установка
#### Клонирование репозитория
```
git clone https://github.com/<your-username>/text-summarizer.git
cd text-summarizer
```
#### Установите зависимости
```
pip install -r requirements.txt 
```
#### Убедитесь, что данные NLTK загружены (обрабатывается автоматически при первом запуске или выполните вручную):
``` 
import nltk
nltk.download('punkt')
```
## Запуск
```
python summarizer.py 
```
## Использование
#### Ввод
Ручной ввод: Вставьте текст в текстовое поле *"Ваш текст"* в интерфейсе **Gradio**.

Загрузка файла: Загрузите файл ` .txt ` с помощью опции загрузки файла.

#### Генерация саммари
Нажмите кнопку *"Submit"* для создания саммари.

Саммари отобразится в текстовом поле ниже.

## Используемая модель: facebook/bart-large-cnn
Было протестировано две модели: ` t5-small ` и ` facebook/bart-large-cnn ` так как они быстрые и лёгкие. Была выбрана модель ` facebook/bart-large-cnn `, потому что эта модель предобучена специально для суммаризации текста, обеспечивая хороший баланс между производительностью и эффективностью. Она хорошо справляется с длинными текстами и генерирует связные, краткие выводы, что делает её подходящей для задачи. А также эта модель сохраняет регистр.

## Пример работы
#### Входные данные
```
A robot is a machine—especially one programmable by a computer—capable of carrying out a complex series of actions automatically.[2] A robot can be guided by an external control device, or the control may be embedded within. Robots may be constructed to evoke human form, but most robots are task-performing machines, designed with an emphasis on stark functionality, rather than expressive aesthetics.

Robots can be autonomous or semi-autonomous and range from humanoids such as Honda's Advanced Step in Innovative Mobility (ASIMO) and TOSY's TOSY Ping Pong Playing Robot (TOPIO) to industrial robots, medical operating robots, patient assist robots, dog therapy robots, collectively programmed swarm robots, UAV drones such as General Atomics MQ-1 Predator, and even microscopic nanorobots. By mimicking a lifelike appearance or automating movements, a robot may convey a sense of intelligence or thought of its own. Autonomous things are expected to proliferate in the future, with home robotics and the autonomous car as some of the main drivers.[3]

The branch of technology that deals with the design, construction, operation, and application of robots,[4] as well as computer systems for their control, sensory feedback, and information processing is robotics. These technologies deal with automated machines that can take the place of humans in dangerous environments or manufacturing processes, or resemble humans in appearance, behavior, or cognition. Many of today's robots are inspired by nature contributing to the field of bio-inspired robotics. These robots have also created a newer branch of robotics: soft robotics.

From the time of ancient civilization, there have been many accounts of user-configurable automated devices and even automata, resembling humans and other animals, such as animatronics, designed primarily as entertainment. As mechanical techniques developed through the Industrial age, there appeared more practical applications such as automated machines, remote-control and wireless remote-control.

The term comes from a Slavic root, robot-, with meanings associated with labor. The word "robot" was first used to denote a fictional humanoid in a 1920 Czech-language play R.U.R. (Rossumovi Univerzální Roboti – Rossum's Universal Robots) by Karel Čapek, though it was Karel's brother Josef Čapek who was the word's true inventor.[5][6][7] Electronics evolved into the driving force of development with the advent of the first electronic autonomous robots created by William Grey Walter in Bristol, England in 1948, as well as Computer Numerical Control (CNC) machine tools in the late 1940s by John T. Parsons and Frank L. Stulen.

The first commercial, digital and programmable robot was built by George Devol in 1954 and was named the Unimate. It was sold to General Motors in 1961 where it was used to lift pieces of hot metal from die casting machines at the Inland Fisher Guide Plant in the West Trenton section of Ewing Township, New Jersey.[8]

Robots have replaced humans[9] in performing repetitive and dangerous tasks which humans prefer not to do, or are unable to do because of size limitations, or which take place in extreme environments such as outer space or the bottom of the sea. There are concerns about the increasing use of robots and their role in society. Robots are blamed for rising technological unemployment as they replace workers in increasing numbers of functions.[10] The use of robots in military combat raises ethical concerns. The possibilities of robot autonomy and potential repercussions have been addressed in fiction and may be a realistic concern in the future.
```
#### Саммари
```
The word "robot" was first used to denote a fictional humanoid in a 1920 Czech-language play R.U.R. (Rossumovi Univerzální Roboti – Rossum's Universal Robots) By mimicking a lifelike appearance or automating movements, a robot may convey a sense of intelligence or thought of its own. The term comes from a Slavic root, robot-, with meanings associated with labor. The first commercial, digital and programmable robot was built by George Devol in 1954 and was named the Unimate. It was sold to General Motors in 1961 where it was used to lift pieces of hot metal from die casting machines at the Inland Fisher Guide Plant in the West Trenton section of Ewing Township, New Jersey. There are concerns about the increasing use of robots and their role in society. A robot is a machine—especially one programmable by a computer—capable of carrying out a complex series of actions automatically. A robot can be guided by an external control device, or the control may be embedded within.
```
