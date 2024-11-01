from classes.entities import Entity, BodyPart


class Human(Entity):
    """class for a human entity"""

    def __init__(self, x: int, y: int, starting_sustenance: int = 100):
        # body parts are defined in a tree structure like so
        body_parts = [
            BodyPart("Upper Torso", 100, 10, starting_sustenance, x, y, required=True, attached=[
                BodyPart("Head", 100, 10, starting_sustenance, x, y, required=True),
                BodyPart("Left Shoulder", 100, 10, starting_sustenance, x, y, attached=[
                    BodyPart("Left Upper Arm", 100, 10, starting_sustenance, x, y, attached=[
                        BodyPart("Left Lower Arm", 100, 10, starting_sustenance, x, y, attached=[
                            BodyPart("Left Hand", 100, 10, starting_sustenance, x, y),
                        ]),
                    ]),
                ]),
                BodyPart("Right Shoulder", 100, 10, starting_sustenance, x, y, attached=[
                    BodyPart("Right Upper Arm", 100, 10, starting_sustenance, x, y, attached=[
                        BodyPart("Right Lower Arm", 100, 10, starting_sustenance, x, y, attached=[
                            BodyPart("Right Hand", 100, 10, starting_sustenance, x, y),
                        ]),
                    ]),
                ]),
                BodyPart("Middle Torso", 100, 10, starting_sustenance, x, y, attached=[
                    BodyPart("Lower Torso", 100, 10, starting_sustenance, x, y, attached=[
                        BodyPart("Left Hip", 100, 10, starting_sustenance, x, y, attached=[
                            BodyPart("Left Upper Leg", 100, 10, starting_sustenance, x, y, attached=[
                                BodyPart("Left Lower Leg", 100, 10, starting_sustenance, x, y, attached=[
                                    BodyPart("Left Foot", 100, 10, starting_sustenance, x, y),
                                ]),
                            ]),
                        ]),
                        BodyPart("Right Hip", 100, 10, starting_sustenance, x, y, attached=[
                            BodyPart("Right Upper Leg", 100, 10, starting_sustenance, x, y, attached=[
                                BodyPart("Right Lower Leg", 100, 10, starting_sustenance, x, y, attached=[
                                    BodyPart("Right Foot", 100, 10, starting_sustenance, x, y),
                                ]),
                            ]),
                        ]),
                    ]),
                ])
            ]),
        ]
        super().__init__(x, y, body_parts, "🧍", "Human")

    def tick(self):
        """called every game tick"""
        super().tick()


def print_entity_data(entity):
    """

    :param entity:
    """
    print(f"hp: {entity.hp}")
    print(f"armor: {entity.armor}")
    print(f"sustenance: {entity.sustenance}")
    print(f"dead: {entity.dead}")
    print(f"decay: {entity.decay}")
    for part in entity.parts:
        print(f"==== {part.name} ====")
        print(f"hp: {part.hp}")
        print(f"armor: {part.armor}")
        print(f"sustenance: {part.sustenance}")
        print(f"dead: {part.dead}")
        print(f"detached: {part.detached}")
        print(f"decay: {part.decay}")
        for attached_part in part.attached_body_parts:
            print(f"==== {attached_part.name} ====")
            print(f"hp: {attached_part.hp}")
            print(f"armor: {attached_part.armor}")
            print(f"sustenance: {attached_part.sustenance}")
            print(f"dead: {attached_part.dead}")
            print(f"detached: {attached_part.detached}")
            print(f"decay: {attached_part.decay}")
    print("==== END =================================")


if __name__ == "__main__":
    human = Human(0, 0)
    while not human.dead:
        human.tick()
        # print data
        print_entity_data(human)
        # input()
    print("Human is dead.")
    # keep ticking until decayed
    while not human.decay >= 100:
        human.tick()
        print_entity_data(human)
        # input()
