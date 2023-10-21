"""
This is a demo player that does nothing. It is used as a template for new players.
"""
import os.path
import sys
from walterplayers.constants import Role

from dotenv import load_dotenv

from walterplayers.base_player import BasePlayer
from walterplayers.constants import Action
from random import choice

class MyPlayer(BasePlayer):
    """ Clase que hereda de la clase padre BasePlayer. """

    """ Método padre de la clase que se ejecuta en cada turno, se encarga de llamar a todas las 
    funciones de la clase para realizar comprobaciones y acciones en un determinado turno. """
    def choose_action(self, find_response):

        self.comprobar()

        return Action.STOP, None


    def comprobar(self):
        if self.find_response.status.life > 125:
            self.compLife125()
        

    def compLife125(self, find_response):
        ''' Se asigna el jugador con menor vida de la zona actual. '''
        current_weakest_enemy = self.get_weakest_enemy(find_response.current_zone)

        ''' En cada zona vecina buscar el enemigo con menor vida y comprobar entre ellos sus puntos 
        de vida para obtener mediante una comparación el que menos vida tiene y a que zona moverse. '''
        weakest_neighbours_zone = None
        weakest_neighbours_enemy = None
        
        for zone in find_response.neighbours_zones:
            weakest_enemy = self.get_weakest_enemy(zone)
            
            if weakest_enemy != None:

                if (weakest_neighbours_enemy == None or weakest_enemy.life < weakest_neighbours_enemy.life):

                    weakest_neighbours_enemy = weakest_enemy
                    weakest_neighbours_zone = zone
        
        if current_weakest_enemy.life == None and weakest_neighbours_enemy.life == None:
            return Action.MOVE, choice(self.get_id_neighbours_zones(find_response))

        elif current_weakest_enemy.life < weakest_neighbours_enemy.life:
            return Action.ATTACK, current_weakest_enemy.id
        
        elif current_weakest_enemy.life > weakest_neighbours_enemy.life:
            return Action.MOVE, weakest_neighbours_zone.zone_id

        elif weakest_neighbours_enemy == None and current_weakest_enemy > 0:
            return Action.ATTACK, current_weakest_enemy.id

        elif current_weakest_enemy == None and weakest_neighbours_enemy > 0:
            return Action.MOVE, weakest_neighbours_zone.zone_id
        
        else:
            return Action.MOVE, choice(self.get_id_neighbours_zones(find_response))
        

    def get_weakest_enemy(self, zone):
        ''' The weakest enemy in zone. '''
        min_life = sys.maxsize
        weakest_enemy = None

        for enemy in self._get_enemies_in_zone(zone):
            if enemy.life <= min_life:
                weakest_enemy = enemy
                min_life = enemy.life

        return weakest_enemy
    

    def _get_enemies_in_zone(self, zone):
        return list(filter(lambda ia: Role.PLAYER == ia.role, zone.ias))


def get_args():
    """ Get arguments from command line """
    import argparse

    parser = argparse.ArgumentParser(description='Demo player')
    parser.add_argument(
        '--env-file',
        type=str,
        default='.env',
        help='Env file to load environment variables from'
    )

    return parser.parse_args()


def main():
    """ Main function """
    args = get_args()

    # check if .env file exists
    if not os.path.exists(args.env_file):
        raise Exception(f"Environment file {args.env_file} does not exist")

    print(f"Loading {args.env_file}")
    load_dotenv(args.env_file)

    player = MyPlayer()
    player.run()


if __name__ == "__main__":
    main()
