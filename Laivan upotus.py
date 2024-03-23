"""
Neljäs projekti: laivanupotuspeli
Tekijä: Arttu Kiviranta
24.11-25.11 tehty valmiiksi

Laivanupotus peli ilman graafista käyttöliittymää
"""


#muutama hyödyllinen globaalimuuttuja

VALID_FIRSTS = ["a","A","b","B","c","C","d","D","e","E","f","F","g","G","h","H","i","I","j","J"]
VALID_SECONDS = ["0","1","2","3","4","5","6","7","8","9"]
AAKKOSET = "  A B C D E F G H I J"


class Grid:
    """Luokka, jolla tehdään 10x10 matriiseja ja tehdään niiden eri operaatioita

    """

    def __init__(self):
        """Ainoa atribuutti on 10x10 matriisi, jota sitten muokkaillaan

        """
        self.__matrix = [["  "]*10 for _ in range(10)]

    def add_locations(self,name,coordinates):
        """Lisää laivojen koordinaatit tietorakenteeseen eli matriisiin

        :param name: laivan nimi, josta merkki eli mark
        :param coordinates: koordinaatit listana
        :return: ei paluuarvoa
        """

        mark = name[0].upper()
        for i in coordinates:
            column = ord(i[0])-ord("A")
            row = int(i[1])
            self.__matrix[row][column] = mark+" "

    def add_marks(self,user_input,mark):
        """Lisää pelaajan laukaukset matriisiin eli syötteen mukaiseen ruutuun tulee haluttu merkki

        :param user_input: käyttäjän syöte
        :param mark: merkki, joka määräytyy sen perusteella osuuko vai ei
        :return: ei paluuarvoa
        """

        column = ord(user_input[0])-ord("A")
        row = int(user_input[1])
        self.__matrix[row][column] = mark+" "

    def print_grid(self):
        """Tulostaa ruudukon halutulla tavalla

        :return:
        """
        print(AAKKOSET)
        for i in range(len(self.__matrix)):
            row_as_string = "".join(self.__matrix[i])
            print(f"{i} {row_as_string}{i}")
        print(AAKKOSET)

    def get_value(self,user_input):
        """Palauttaa mielenkiintoisen ruudun arvon

        :param user_input: lukee käyttäjän syötteen tai jonkin tiedon, joka kertoo rivin ja sarakkeen
        :return: arvo kohdassa XY
        """
        column = ord(user_input[0])-ord("A")
        row = user_input[1]
        value = self.__matrix[row][column]
        return value


class Laiva:
    """Luokka, jolla tehdään laivoja ja niiden eri operaatioita

    """

    def __init__(self,name):
        """Attribuutteina ovat nimi sekä koordinaatit. Ainoastaan nimi otetaan parametrina ja koordinaatit lisätään
        erikseen metodilla. En tiedä mistä syystä suoraan lisääminen toimi kovin vaikeasti.

        :param name:
        """
        self.__name = name
        self.__coordinates = []

    def add_coordinates(self,coordinates):
        """Lisää laivalle koordinaait, joiden avulla vuorovaikutetaan Grid olioiden kanssa

        :param coordinates: Laivan koordinaatit listana
        :return: ei paluuarvoa
        """
        for i in coordinates:
            self.__coordinates.append(i)


    def get_name(self):
        """aika yksiselitteinen, mutta automaattitesteri valitti docstring kommenteista

        :return: nimi
        """
        return self.__name

    def get_coordinates(self):
        """aika yksiselitteinen, mutta automaattitesteri valitti docstring kommenteista

        :return: koordinaatit
        """
        return self.__coordinates


def create_objects(object_creator):
    """Tällä luodaan ohjelman tekstistä lukemat oliot. Tämä on ehkä ohjelman tärkein funktio, koska tämä palauttaa
    kolme erittäin tärkeätä listaa. Toki kaksi niistä ovat vähän niin kuin samat, mutta tajusin sen vasta nyt.

    :param object_creator: Lista, jossa parillinen indeksi (ja 0) tarkoittaa Laivan nimeä ja pariton indeksi
    tarkoittaa listaa edellisen indeksin koordinaateista
    :return: palauttaa listan nimistä ja olioista. Nämä kaksi listaa ovat ilmeisesti samat pythonin mielestä.
    Ainakin list_of_names:lle voi käyttää Laiva luokan metodeja. Palauttaa myös list_of_coordinates, jolla on
    iso rooli myöhemmin. On tärkeää, että list_of_names[i] nimeä vastaavat koordinaatit löytyy samalla i arvolla
    list_of_coordinatesista.
    """
    list_of_names = []
    list_of_coordinates = []
    list_of_laivas = []
    for i in range(len(object_creator)):
        if i%2 == 0:
            list_of_names.append(object_creator[i])
        else:
            list_of_coordinates.append(object_creator[i])
    if len(list_of_names) != len(list_of_coordinates):
        print("Miten edes mahdollista?")
    else:
        for i in range(len(list_of_names)):
            list_of_names[i] = Laiva(list_of_names[i])
            list_of_names[i].add_coordinates(list_of_coordinates[i])
            list_of_laivas.append(list_of_names[i])

    return list_of_names, list_of_coordinates, list_of_laivas


def main():
    file_name = input("Enter file name: ")
    file_checker = []
    object_creator = []
    set_of_taken_shots = set()
    set_of_targets = set()
    better_list_of_coordinates = []
    hit_tracker = []

    #Avataan tiedosto ja tehdään virhetarkistukset<-- en keksinyt miten toimisi helposti mainin ulkopuolella

    try:
        file_in_use = open(file_name,mode="r")
        for line in file_in_use:
            modded_line = line.replace("\n","")
            split_line = modded_line.split(";")


            if split_line[0] != "":
                object_creator.append(split_line[0])
                object_creator.append(split_line[1:])

            for coordinate in split_line[1:]:
                if len(coordinate) != 2 or coordinate[0] not in VALID_FIRSTS or coordinate[1] not in VALID_SECONDS:
                    print("Error in ship coordinates!")
                    return
            for first_index in split_line[1:]:
                file_checker.append(first_index)


        if len(set(file_checker)) != len(file_checker):
            print("There are overlapping ships in the input file!")

            return

        #Luodaan Laivat sekä listat

        list_of_names, list_of_coordinates, list_of_laivas = create_objects(object_creator)

        #Jatketaan apulistaa hit_tracker ja tehdään siitä halutun mittainen

        for i in range(len(list_of_coordinates)):
            hit_tracker.append([])

        #Luodaan kaksi Gridiä eli 10x10 matriisia

        grid_for_shooting = Grid()
        grid_of_targets = Grid()

        #Luodaan setti kaikkien laivojen koordinaateista

        for first_index in list_of_coordinates:
            for second_index in first_index:
                better_list_of_coordinates.append(second_index)
        for i in better_list_of_coordinates:
            set_of_targets.add(i)

        #Tässä kohdassa lisätään kohderuudukkoon kaikki tekstistä luetut merkit haluttuihin paikkoihin

        for i in list_of_laivas:
            grid_of_targets.add_locations(i.get_name(),i.get_coordinates())

        #Itse gameplay looppi

        while True:
            #Alkuun tulostetaan ruudukko
            print()
            grid_for_shooting.print_grid()
            print()

            #Tarkistetaan onko pelaaja voittanut

            if set_of_targets.issubset(set_of_taken_shots):
                print("Congratulations! You sank all enemy ships.")
                break

            #Kysytään syöte, jolle tosiaan keksittiin ihan viimeisenä asiana koko projektissa tuo upper() metodi

            user_input = input("Enter place to shoot (q to quit): ").upper()

            #suoritetaan virhetarkistukset

            if "q" in user_input or "Q" in user_input:
                print("Aborting game!")
                break
            if len(user_input) != 2 or user_input[0] not in VALID_FIRSTS or user_input[1] not in VALID_SECONDS:
                print("Invalid command!")
            else:

                #suoritetaan itse peli (ja yksi virhe tarkistuksista)

                if user_input in set_of_taken_shots:
                    print("Location has already been shot at!")
                else:
                    set_of_taken_shots.add(user_input)

                    if user_input in set_of_targets:
                        mark = "X"
                        grid_for_shooting.add_marks(user_input,mark)

                        for i in range(len(list_of_coordinates)):

                            if user_input in list_of_coordinates[i]:
                                hit_tracker[i].append(user_input)

                                if sorted(hit_tracker[i]) == sorted(list_of_coordinates[i]):
                                    mark = list_of_names[i].get_name()[0].upper()

                                    for coordinate in list_of_coordinates[i]:
                                        grid_for_shooting.add_marks(coordinate,mark)

                                    print(f"You sank a {list_of_names[i].get_name()}!")

                    else:
                        mark = "*"
                        grid_for_shooting.add_marks(user_input, mark)

    except OSError:
        print("File can not be read!")


if __name__ == "__main__":
    main()
