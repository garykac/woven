
# Spell Cards - Prototype 2

Note: These spells were inadvertently made too complicated because they jump from simple (2-block without an Element) to complex (4-block with an Element). There are basically no 3-block spells because of this error. Oops.

## Base Spells

### Link

```
 X X
```
No effect, but may be used to chain 2 spells together.

### Target

```
 A
   B
```

Target up to <n> spaces away where n = B-A. Negative values = 0
(?: Target up to <n> spaces away where n = lowest of A or B.)

### Split

```
   A
 B   C
```

Spell must link in at A and out from B and C
If A=1,2,3, then B executes first, otherwise C executes first.

	
## Instant Spells

These spells come into effect as soon as the mana dice are placed
and stay in effect until the counter reaches zero. At that point
all the mana dice for the spell are removed. If any mana dice were
shared with other instant spells, then they collapse immediately
and their dice are removed as well.

### Advance - Air

```
     X
     A X
   @
```
Element: Air

Reveal new spell cards until an Air spell is revealed.

### Advance - Earth

```
   X
 X A
     @
```

Element: Earth

Reveal new spell cards until an Earth spell is revealed.

### Advance - Fire

```
 @
   A X
   X
```

Element: Fire

Reveal new spell cards until a Fire spell is revealed.

### Advance - Water

```
     @
 X A
   X
```

Element: Water

Reveal new spell cards until a Water spell is revealed.

### Move Dice - Air

```
     X
 @   A
   X
```

Element: Air

Move a die in your matrix into an unassigned block in your matrix.
You may repeat this up to A times.
Ignore constraints when placing the dice.

### Move Dice - Fire

```
   X
 X   @
 A
```

Element: Fire

Move a die in your matrix into an unassigned block in your matrix.
You may repeat this up to A times.
Ignore constraints when placing the dice.

### Move Dice - Earth

```
 X A
     X
   @
```

Element: Earth

Move a die in your matrix into an unassigned block in your matrix.
You may repeat this up to A times.
Ignore constraints when placing the dice.

### Move Dice - Water

```
   @
 A
   X X
```

Element: Water

Move a die in your matrix into an unassigned block in your matrix.
You may repeat this up to A times.
Ignore constraints when placing the dice.

### Swap Dice - Air

```
   A
 X   X
   @
```

Element: Air

Rearrange up to A dice that have already been added to your matrix.
Ignore constraints when placing the dice.

### Swap Dice - Fire

```
   A
 @   X
   X
```

Element: Fire

Rearrange up to A dice that have already been added to your matrix.
Ignore constraints when placing the dice.

### Swap Dice - Earth

```
   @
 X   X
   A
```

Element: Earth

Rearrange up to A dice that have already been added to your matrix.
Ignore constraints when placing the dice.

### Swap Dice - Water

```	
   A
 X   @
   X
```

Element: Water

Rearrange up to A dice that have already been added to your matrix.
Ignore constraints when placing the dice.

## Spells

These spells must be activated before they take effect.

### Long Target (Air)
```
 X A B
 @
```

Element: Air

Target up to <n> spaces away where n = A+B

### Long Target (Fire)
```
   @
 X A B
```

Element: Fire

Target up to <n> spaces away where n = A+B

### Long Target (Earth)
```
 @
 X A B
```

Element: Earth

Target up to <n> spaces away where n = A+B

### Long Target (Water)
```
 X A B
   @
```

Element: Water

Target up to <n> spaces away where n = A+B

### Fire Burst
```
 X   X
 A   B
   @
```

Element: Fire

Fire damage of max(a,B) to target.

### Rock Smash
```
   X
 A X B
   @
```

Element: Earth

Earth damage of max(a,B) to target.

### Hurricane
```
   X X
 A   B
   @
```

Element: Air

Air damage of max(a,B) to target.

### Water Blast
```
 X X
 A   B
   @
```

Element: Water

Water damage of max(A,B) to target.

### Shield Earth
```
 X X @
   X A
```

Element: Earth

Defend against A points of attack

### Boulder Roll
```
 @ X X
 A X
```

Element: Earth

Cause A points of Earth damage

### Shield Air
```
 X X   @
     X A
```

Element: Air

Defend against A points of attack

### Attack Air:
```
 @   X X
 A X
```

Element: Air

Cause A points of Air damage

### Shield Water
```
 X X   A
     X @
```

Element: Water

Defend against A points of attack

### Attack Water:
```
 A   X X
 @ X
```

Element: Water

Cause A points of Water damage

### Shield Fire
```
 X   X @
   X   A
```

Element: Fire

Defend against A points of attack

### Flambeau (Attack Fire):
```
 @ X   X
 A   X
```

Element: Fire

Cause A points of Fire damage

### Shield - Large Earth
```
 B A
 X @ X
 X
```

Element: Earth

Block <n> points of A, F or W attack, where n = A + B 

### Shield - Large Air
```
 X
 X @ X
 B A
```

Element: Air

Block <n> points of F, E or W attack, where n = A + B 

### Shield - Large Water
```
 X B
   @ A
       X
     X
```

Element: Water

Block <n> points of A, F or E attack, where n = A + B 

### Shield - Large Fire
```
     B X
   A @
 X
   X
```

Element: Fire

Block <n> points of A, E or W attack, where n = A + B 

### Anchor
```
 B
   X X
   @ A
   X
```

Element: Water

While in effect, the target will not be affected by spells
that change location (Push, Teleport, ...).
Strength of this effect is A, or A+B when resisting Water spells

### Anchor
```
 X @ B X
 A X
```

Element: Earth

While in effect, the target will not be affected by spells
that change location (Push, Teleport, ...).
Strength of this effect is A, or A+B when resisting Earth spells

### Anchor
```
 X @ B
 A X   X
```

Element: Air

While in effect, the target will not be affected by spells
that change location (Push, Teleport, ...).
Strength of this effect is A, or A+B when resisting Air spells

### Anchor
```
 X @ X
 A X
   B
```

Element: Fire

While in effect, the target will not be affected by spells
that change location (Push, Teleport, ...).
Strength of this effect is A, or A+B when resisting Fire spells

### Pointy Rock Shards
```
   @   X
 X X   X
     A
```

Element: Earth

Double damage to magical barriers/elemental beings of A, F and W.
Half damage to Earth barriers. Normal damage to mages.

### Piercing Attack
```
 X   @
 X   X X
   A
```

Element: Air

Double damage to magical barriers/elemental beings of F, E and W.
Half damage to Air barriers. Normal damage to mages.

### Piercing Attack
```
 X @
   X   A
   X X
```

Element: Fire

Double damage to magical barriers/elemental beings of A, E and W.
Half damage to Fire barriers. Normal damage to mages.

### Piercing Attack
```
   X X
   X   A
 X @
```

Element: Water

Double damage to magical barriers/elemental beings of A, F and E.
Half damage to Water barriers. Normal damage to mages.

### Clone Air
```
 X X @ X X
     A
```

Element: Air

Copy an Air spell from another player. You may cast the cloned spell
at most A times. If you have already cloned an Air spell, then:

* (1) if you are cloning a different Air spell, then cancel the prev
* (2) if cloning the same, then increase the usage count by A.

### Clone Fire
```
 X X
     A
     @ X X
```

Element: Fire

Copy a Fire spell from another player. You may cast the cloned spell
at most A times. If you have already cloned a Fire spell, then:

* (1) if you are cloning a different Fire spell, then cancel the prev
* (2) if cloning the same, then increase the usage count by A.

### Clone Water
```
     @ X X
     A
 X X
```

Element: Water

Copy a Water spell from another player. You may cast the cloned spell
at most A times. If you have already cloned a Water spell, then:

* (1) if you are cloning a different Water spell, then cancel the prev
* (2) if cloning the same, then increase the usage count by A.

### Clone Earth
```
 X
   X A
   @ X
       X
```

Element: Earth

Copy an Earth spell from another player. You may cast the cloned spell
at most A times. If you have already cloned an Earth spell, then:

* (1) if you are cloning a different Earth spell, then cancel the prev
* (2) if cloning the same, then increase the usage count by A.

### Entangle
```
   X
 X @ A B
   X
```

Element: Earth

Target creature is magically trapped at location for B turns
Strength of this spell is A (for dispel).

### Air Trap
```
   X B
 X @ A
   X
```

Element: Air

Target creature is magically trapped at location for B turns
Strength of this spell is A (for dispel).

### Ice Cube
```
   X
 X @ A
   X   B
```

Element: Water

Target creature is magically trapped at location for B turns
Strength of this spell is A (for dispel).

### Ring of Fire
```
   X   B
 X @ A
   X
```

Element: Fire

Target creature is magically trapped at location for B turns
Strength of this spell is A (for dispel).

### Dispel Earth
```
   X
 X   A
   @   B
     X
```

Element: Earth

Cancels the effect of a spell on the targeted creature or location.
The effect is dispelled if the strength of this spell is greater or
equal to the strength of the spell being dispelled.
When dispelling A,F,W spells, strength = A
When dispelling E spells, strength = A+B
Any targets in the dispelled location are canceled.

### Dispel Air
```
 X
   X   B
   @ A
   X
```

Element: Air

Cancels the effect of a spell on the targeted creature or location.
The effect is dispelled if the strength of this spell is greater or
equal to the strength of the spell being dispelled.
When dispelling F,E,W spells, strength = A
When dispelling A spells, strength = A+B
Any targets in the dispelled location are canceled.

### Dispel Water
```
 X
   X
   @ A
   X   B
```

Element: Water

Cancels the effect of a spell on the targeted creature or location.
The effect is dispelled if the strength of this spell is greater or
equal to the strength of the spell being dispelled.
When dispelling A,F,E spells, strength = A
When dispelling W spells, strength = A+B
Any targets in the dispelled location are canceled.

### Dispel Fire
```
 X
   B
     X
     @ A
     X
```

Element: Fire

Cancels the effect of a spell on the targeted creature or location.
The effect is dispelled if the strength of this spell is greater or
equal to the strength of the spell being dispelled.
When dispelling A,E,W spells, strength = A
When dispelling F spells, strength = A+B
Any targets in the dispelled location are canceled.

### Take Your Breath Away
```
 A
   B @ X
 C   X
```

Element: Air

Attack targetted CREATURE with strength min(A,B,C).
Any mana dice lost in the attack are added to your pool instead of
returning to the commons.

### Leech
```
 C   X
   B @ X
 A
```

Element: Earth

Attack targetted CREATURE with strength min(A,B,C).
Any mana dice lost in the attack are added to your pool instead of
returning to the commons.

### Vampyric Suck
```
 X @ A
   X   B
         C
```

Element: Water

Attack targetted CREATURE with strength min(A,B,C).
Any mana dice lost in the attack are added to your pool instead of
returning to the commons.

### Dessicate
```
         C
   X   B
 X @ A
```

Element: Fire

Attack targetted CREATURE with strength min(A,B,C).
Any mana dice lost in the attack are added to your pool instead of
returning to the commons.

### Levitate
```
   X
   X   X
 X @ A
```

Element: Air

Player may move over <n> spaces of any terrain as if
it were normal terrain.

### Water Walker
```
       X
   X   X
 X @ A
```

Element: Water

Player may move over <n> spaces of water terrain as if
it were normal terrain.

### Earth Mover
```
 X   X
   A @ X
   X
```

Element: Earth

Player may move over <n> spaces of forest terrain as if
it were normal terrain.

### Blazing Trail
```
 X @ A
   X   X
       X

```
Element: Fire

Player may move over <n> spaces of normal terrain.

### Summon Minion - Fire
```
 @
 X A
     X
       B
```

Element: Fire

Summon a Fire minion at the targeted location.
Initial attack = A, defense = B.
If you already control a Fire minion, then the previous one is dispelled.

### Summon Minion - Water
```
 B     A
   X X @
```

Element: Water

Summon a Water minion at the targeted location.
Initial attack = A, defense = B.
If you already control a Water minion, then the previous one is dispelled.

### Summon Minion - Air
```
 B   @
   X   A
     X
```

Element: Air

Summon a Air minion at the targeted location.
Initial attack = A, defense = B.
If you already control a Air minion, then the previous one is dispelled.

### Summon Minion - Earth
```
 X
 B
   X
   @ A
```

Element: Earth

Summon a Earth minion at the targeted location.
Initial attack = A, defense = B.
If you already control a Earth minion, then the previous one is dispelled.

### Strengthen Minion - Fire
```
 @ X
     A
       B
       X
```

Element: Fire

Increase targeted minion's attack strength by A.
If targeted minion is Fire, then also strengthen defense by B.

### Strengthen Minion - Water
```
 X A
 @   B
     X
```

Element: Water

Increase targeted minion's attack strength by A.
If targeted minion is Water, then also strengthen defense by B.

### Strengthen Minion - Air
```
 X
   A
 @   X
   B
```

Element: Air

Increase targeted minion's attack strength by A.
If targeted minion is Air, then also strengthen defense by B.

### Strengthen Minion - Earth
```
   X
 A   B
 X @ X
```

Element: Earth

Increase targeted minion's attack strength by A.
If targeted minion is Earth, then also strengthen defense by B.

### Summon Air Elemental
```
 X @
   A C
     B
     X
```

Element: Air

Summon an Air Elemental at the target location.
Once summoned, Elemental Daemons cannot be controlled. They always
attack nearest wizard. They can only move 1 space.
Initial attack = A, defense = B+C

### Summon Earth Elemental
```
 X @
   A C X
   B
```

Element: Earth

Summon an Earth Elemental at the target location.
Once summoned, Elemental Daemons cannot be controlled. They always
attack nearest wizard. They can only move 1 space and cannot cross water.
Initial attack = A, defense = B+C

### Summon Fire Elemental
```
   A B X
 X @ C
```

Element: Fire

Summon a Fire Elemental at the target location.
Once summoned, Elemental Daemons cannot be controlled. They always
attack nearest wizard. They can only move 1 space and cannot cross water.
Initial attack = A, defense = B+C

### Summon Water Elemental
```
 X @ C
   B A X
```

Element: Water

Summon a Water Elemental at the target location.
Once summoned, Elemental Daemons cannot be controlled. They always
attack nearest wizard. They can only move 1 space and cannot cross mountains.
Initial attack = A, defense = B+C

### Wind Force
```
 X @
 X X
 A X
```

Element: Air

Target creature is pushed into a neighboring space chosen by the spellcaster.
The space must be unoccupied, but the target is moved there regardless of
whether or not they could normally have traveled there.
If the target is pushed into a space with fields, then they may be pushed
into another neighboring space (repeat as necessary for max A spaces).

### Rock Nudge
```
 @ X
 X A
 X X
```

Element: Earth

Target creature is pushed into a neighboring space chosen by the spellcaster.
The space must be unoccupied, but the target is moved there regardless of
whether or not they could normally have traveled there.
If the target is pushed into a space with forest, then they may be pushed
into another neighboring space (repeat as necessary for max A/2 spaces).

### Wet Slide
```
 X
 @ A X
   X X
```

Element: Water

Target creature is pushed into a neighboring space chosen by the spellcaster.
The space must be unoccupied, but the target is moved there regardless of
whether or not they could normally have traveled there.
If the target is pushed into a space with water, then they may be pushed
into another neighboring space (repeat as necessary for max A spaces).

### Flaming Shove
```
 X
   X X
 @ A X
```

Element: Fire

Target creature is pushed into a neighboring space chosen by the spellcaster.
The space must be unoccupied, but the target is moved there regardless of
whether or not they could normally have traveled there.

### Teleport Self - Air
```
   X   X
 X @ X   X
```

Element: Air

Teleport the spellcaster to the target location.
Target location must be unoccupied

### Teleport Self - Earth
```
   X
 X   X @ X
       X
```

Element: Earth

Teleport the spellcaster to the target location.
Target location must be unoccupied

### Teleport Self - Water
```
 X     @ X
   X   X
     X
```

Element: Water

Teleport the spellcaster to the target location.
Target location must be unoccupied

### Teleport Self - Fire
```
     X
   X   X
 X     @ X	
```

Element: Fire

Teleport the spellcaster to the target location.
Target location must be unoccupied

### Teleport Other - Air
```
   X   X   X
 X @ X   X
```

Element: Air

Requires 2 targets: SRC and DST.
Teleport the creature at SRC to DST.
Target location must be unoccupied.

### Teleport Other - Earth
```
 X   X
   X   X @ X
         X
```

Element: Earth

Requires 2 targets: SRC and DST.
Teleport the creature at SRC to DST.
Target location must be unoccupied.

### Teleport Other - Water
```
   X     @ X
 X   X   X
       X
```

Element: Water

Requires 2 targets: SRC and DST.
Teleport the creature at SRC to DST.
Target location must be unoccupied.

### Teleport Other - Fire
```
       X
 X   X   X
   X     @ X	
```

Element: Fire

Requires 2 targets: SRC and DST.
Teleport the creature at SRC to DST.
Target location must be unoccupied.

### Teleswap - Air
```
 X   X   X   X
   X @ X   X
```

Element: Air

Requires 2 targets: TGTA and TGTB.
Exchange the location of the creature at TGTA with that of TGTB.
There must be a CREATURE at each location or the spell has no effect.

### Teleswap - Earth
```
 X   X       X
   X   X @ X
         X
```

Element: Earth

Requires 2 targets: TGTA and TGTB.
Exchange the location of the creature at TGTA with that of TGTB.
There must be a CREATURE at each location or the spell has no effect.

### Teleswap - Water
```
 X   X     @ X
   X   X   X
         X
```

Element: Water

Requires 2 targets: TGTA and TGTB.
Exchange the location of the creature at TGTA with that of TGTB.
There must be a CREATURE at each location or the spell has no effect.

### Teleswap - Fire
```
         X
   X   X   X
 X   X     @ X	
```

Element: Fire

Requires 2 targets: TGTA and TGTB.
Exchange the location of the creature at TGTA with that of TGTB.
There must be a CREATURE at each location or the spell has no effect.

### Mirror Obscura
```
 X   X
 X X
 @ X
```

Element: Air

The target of this spell and its neighboring hexes cannot be targeted
by future spells. Existing targets remain in place.

### Obfuscate
```
 X   X
   X X
   X @
```

Element: Earth

The target of this spell and its neighboring hexes cannot be targeted
by future spells. Existing targets remain in place.

### Smokey Haze
```
       X
   X X @
 X   X
```

Element: Fire

The target of this spell and its neighboring hexes cannot be targeted
by future spells. Existing targets remain in place.

### Obscuring Mist
```
 X
 @ X X
   X   X
```

Element: Water

The target of this spell and its neighboring hexes cannot be targeted
by future spells. Existing targets remain in place.

### Recall - Air
```
 X X   X
     X @
   X
```

Element: Air

Search the spell discard pile for an Air spell and place it in front
of you as an available spell. The first person to cast this spell
will gain ownership. You may only have 1 recalled Air spell at a time.

### Recall - Earth
```
 X X   X
   @ X 
       X
```

Element: Earth

Search the spell discard pile for a Earth spell and place it in front
of you as an available spell. The first person to cast this spell
will gain ownership. You may only have 1 recalled Earth spell at a time.

### Recall - Fire
```
 X @
 X   X
   X
 X
```

Element: Fire

Search the spell discard pile for a Fire spell and place it in front
of you as an available spell. The first person to cast this spell
will gain ownership. You may only have 1 recalled Fire spell at a time.

### Recall - Water
```
 X
 X   X
   X
 @   X
```

Element: Water

Search the spell discard pile for a Water spell and place it in front
of you as an available spell. The first person to cast this spell
will gain ownership. You may only have 1 recalled Water spell at a time.

### Research - Air
```
 X X   X X
     X @
   X
```

Element: Air

Search the spell deck for an Air spell and place it in front
of you as an available spell. The first person to cast this spell
will gain ownership. You may only have 1 recalled Air spell at a time.

### Research - Earth
```
 X X   X
   @ X 
       X X
```

Element: Earth

Search the spell deck for a Earth spell and place it in front
of you as an available spell. The first person to cast this spell
will gain ownership. You may only have 1 recalled Earth spell at a time.

### Research - Fire
```
 X @
 X   X X
   X
 X
```

Element: Fire

Search the spell deck for a Fire spell and place it in front
of you as an available spell. The first person to cast this spell
will gain ownership. You may only have 1 recalled Fire spell at a time.

### Research - Water
```
 X
 X   X X
   X
 @   X
```

Element: Water

Search the spell deck for a Water spell and place it in front
of you as an available spell. The first person to cast this spell
will gain ownership. You may only have 1 recalled Water spell at a time.


## Other Spells

These spells were added later and not part of the prototypes.

### Terraform

Change terrain type
	
### Disrupt

Person with most matching element in their matrix loses <n> dice
	
### Target Adjust

Move existing target by 1 space any direction
