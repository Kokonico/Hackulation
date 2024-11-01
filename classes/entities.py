"""file for all entity classes"""

from classes.shared import BaseObject


class BodyPart(BaseObject):
    """class for a single body part"""

    def __init__(self, name: str, hp: int, armor: int, sustenance: int, x: int, y: int, required: bool = False,
                 attached: list | None = None, min_sustenance: int = 10):
        super().__init__(x, y, physical=False)
        self.name = name
        self.hp = hp
        self.armor = armor
        self.sustenance = sustenance
        self.detached = False
        self.dead = False
        self.decay = 0
        self.required = required
        self.min_sustenance = min_sustenance
        self.attached_body_parts = attached if attached else []
        # look for attached body parts, if any of them are required, this part is also required
        for part in self.attached_body_parts:
            if part.required:
                self.required = True

    def tick(self):
        """called every game tick"""
        if self.detached and not self.dead:
            self.hp -= 1
            self.decay += 1
        elif self.dead:
            self.decay += 2 if self.detached else 1  # if detached, decay faster

        # passive sustenance usage
        self.sustenance -= 1

        self.sustenance = 0 if self.sustenance < 0 else self.sustenance

        # attempt to heal with sustenance
        if self.hp < 100 and self.sustenance > 0:
            self.hp += 1
            self.sustenance -= 1
        elif self.hp >= 100 and self.sustenance > self.min_sustenance:
            # hp is full, check for body parts to give sustenance to
            for part in self.attached_body_parts:
                if part.hp < 100 and self.sustenance > self.min_sustenance and part.sustenance < 100 and part.sustenance + 1 <= self.sustenance or part.required and part.sustenance < part.min_sustenance:
                    part.sustenance += 1
                    self.sustenance -= 1
        else:
            # no sustenance, lose hp
            self.hp -= 1

        if self.hp >= 100:
            self.hp = 100
        elif self.hp <= 0:
            self.hp = 0
            self.armor = 0
            self.sustenance = 0
            self.dead = True

        if self.decay < 0:
            self.decay = 0

        # tick attached body parts
        for part in self.attached_body_parts:
            part.tick()

    def __str__(self):
        return f"""
        BodyPart: {self.name}
        hp: {self.hp}
        armor: {self.armor}
        sustenance: {self.sustenance}
        dead: {self.dead}
        attached body parts: {len(self.attached_body_parts)}
        """


class Body(BaseObject):
    """class for an entire body"""

    def __init__(self, x: int, y: int, body_parts: list, visual: str):
        super().__init__(x, y)
        self.parts = body_parts
        self.sustenance = 100
        self.visual = visual
        self.decay = 0
        self.hp = 100
        self.original_required_parts = [part for part in self.parts if part.required]

    def tick(self) -> list:
        """called every game tick, returns objects that have been ejected from the body"""
        ejected_parts = []

        # give sustenance to all parts (the body object does not use sustenance)

        if self.sustenance > 0:
            for part in self.parts:
                if part.sustenance < 100 and self.sustenance > 0:
                    part.sustenance += 1
                    self.sustenance -= 1

        for part in self.parts:
            part.tick()

        try:
            self.decay = sum(part.decay for part in self.parts) / len(self.parts)
        except ZeroDivisionError:
            self.decay = 100
        try:
            self.hp = sum(part.hp for part in self.parts) / len(self.parts)
        except ZeroDivisionError:
            self.hp = 0

        # look for detached parts
        for part in self.parts:
            if part.detached:
                ejected_parts.append(part)
                self.parts.remove(part)

        # look for if any required parts are dead
        for part in self.parts:
            if part.required and part.dead:
                self.die()
        # look for any missing required parts
        for required_part in self.original_required_parts:
            if required_part not in self.parts:
                self.die()

        return ejected_parts

    def __str__(self):
        strings = [str(part) for part in self.parts]
        return f"""
        Body: {self.visual}
        decay: {self.decay}
        sustenance: {self.sustenance}
        parts: {"\n\n".join(strings)}
        """

    def visual(self):
        """return the visual representation of the body"""
        return self.visual

    def die(self):
        """kill the body, don't decay, just die"""
        self.sustenance = 0
        for part in self.parts:
            part.hp = 0
            part.dead = True
            part.sustenance = 0


class Entity(Body):
    """class for an entity"""

    def __init__(self, x: int, y: int, body_parts: list, visual: str, name: str):
        super().__init__(x, y, body_parts, visual)
        self.name = name
        self.armor = 0
        self.dead = False

    def tick(self):
        """called every game tick"""
        ejected = super().tick()
        if self.hp <= 0:
            self.dead = True
            if self.decay > 100:
                del self

        return ejected

    def __str__(self):
        return f"""
        Entity: {self.name}
        armor: {self.armor}
        dead: {self.dead}
        {super().__str__()}
        """

    def visual(self):
        """return the visual representation of the entity"""
        return self.visual
