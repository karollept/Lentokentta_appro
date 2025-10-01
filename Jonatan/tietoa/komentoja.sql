#oikeudet tietokantaan:
GRANT ALL PRIVILEGES ON flight_game* TO 'JonatanGM'@'localhost';


#helsinki vantaan yhteydet,  id määrittää mikä kenttä
          SELECT nimi FROM kenttä
          inner join yhteys on kenttä.id=yhteys_id
          where yhteys.kenttä_id="1";
