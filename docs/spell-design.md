# Spell cards

A spell card contains the following information:

* Name.
* Pattern.
* Effect.
* (Optional) Flavor text.

## Name

An evocative title for the spell.

## Pattern

This is the representation of the layout that must be created in the mage's tapestry in order to cast this spell.

Patterns contain zero or more ELEMENTs.
Patterns that do not contain any ELEMENT are NEUTRAL.

Patterns specify one or more THREADs that are required for this spell. Whenever a mage places a thread, they may cast any one spell they control whose pattern is completed by that thread.

## Effect

Spell effects have three parts:

1. An effect that occurs at the time the spell is cast.
2. A permanent effect for when the spell has one or more charges on it.
3. A reactionary effect that requires a charge on the spell and costs something (often a charge) to use.

## Design space expansions for Spells

* Multiple elements in pattern
* Constraints within the squares of the pattern

# Spell Categories

# Primary Categories

| Category           | Element | Description |
| ------------------ | ------- | ----------- |
| Attack Mage        | Fire    | Attack other mage. |
| Attack Tendril     | Fire    | Attack other mage's tendril. |
| Attack Charge      | Air     | Attack shield/other charged spell. |
| Attack Tapestry    | Air     | Attack tapestry by blocking squares. |
| Create Tendril     | Water   | Create new tendril at current location. |
| Defend Mage        | Earth   | Defend self against attacks. |
| Defend Tendril     | Earth   | Defend tendrils from attack. |
| Defend Charge      | Earth   | Defend charges from attack. |
| Defend Tapestry    | Earth   | Defend tapestry from attack. |
| Move Mage          | Air     | Move self on map. |
| Move Astral        | Water   | Move self via astral plane |
| Move Tendril       | Water   | Move one of your tendrils on map. |
| Move Other Mage    | Air     | Move another mage on the map. |
| Move Other Tendril | Water   | Move another mage's tendril on the map. |
| Modify Tapestry    | Water   | Adjust threads in tapestry. |

## Additional Attributes

| Category | Element | Description |
| -------- | ------- | ----------- |
| Terrain  |         | Spell effect depends on current terrain. |

# Element properties

In general, if an element is good at one aspect, the opposing element is bad at the same.

## Fire
General: active, light (weight), bright, thin, movement, transformation, change, destruction, hot

* Enemy: Water (tendril create/move)
* Primary Ability: Attack Mage
* Anti-Water Ability: Attack Tendril
* Secondary Ability: Move Mage (Air)
* Tertiary Ability: Defend (Earth)
* Tendrils: few, fast, consumed

Fire likes blast damage, cheap but difficult-to-control bursts at single targets that are consumed by the spell. Fire doesn't like charges, because they're too slow -- Fire wants its effects now. Fire isn't good at manipulating tendrils, as it's too much work. Good fire play needs tendril support from another color.

Fire hates other tendrils, and has the best tendril-killing spells around.

For patterns, fire likes diagonals and distance; many fire spells need multiple cards (but only one or two mana).

## Air
General: active, light (weight), bright, thin, movement, travel, flying, finding, teaching, imagination, sound

* Enemy: Earth (defend)
* Primary Ability: Move Mage
* Anti-Earth Ability: 
* Secondary Ability: Move Tendril (Water)
* Tertiary Ability: Attack Mage/Tendril (Fire)
* Tendrils: few, fast, persistent

Air likes precision effects to single targets, and quick, flowing movement. Swapping positions with a tendril, for example. Air likes permanent charges, where you have an ability for as long as you hold the charge. Air is great at quickly moving a single tendril around -- warping it to another forest, or quickly through the plains. Air is terrible at protection and reactions, so hopefully your motion can keep you safe or you can branch into another color for a shield.

Air hates shield and protection effects, and has lots of ways to blow away charges and move your opponents' tendrils away from their positions.

For patterns, air likes close diagonals; an air symbol with lots of space around it can cast and combo a bunch of spells by itself.

## Water
General: passive, heavy, dark, thick, flowing, living, cleansing, psychic, scrying/mirrors, dreams, cool

* Enemy: Fire (damage)
* Primary Ability: Create Tendril, Move Tendril
* Anti-Fire Ability: 
* Secondary Ability: Defend (Earth)
* Tertiary Ability: Move Mage (Air)
* Tendrils: many, slow, consumed

Water likes sending a wave of tendrils out to break upon its opponents. Move all your tendrils two MPs, then consume tendrils to move co-located mages two MPs, for example. Water likes spending its tendrils as charges, instead of holding charges on spells. It's great at moving a bunch of tendrils around, pulling strings all over the map. Water has a tough time doing damage -- best it can do is warp you back up to the astral plane or push you around. If you want to kill someone, branch into another color.

Water hates damage effects, and has lots of ways to redirect it or punish your opponent for using it. (If a water mage is going down, you're going down with them.)

For patterns, water likes connections; orthogonal or diagonal doesn't matter to water, as long as the spell leaves a stream of thread on your tapestry.

## Earth
General: passive, heavy, dark, thick, stability, quiet, birth, fertility, strength, cool, solid

* Enemy: Air (movement)
* Primary Ability: Defend Mage, Defend Tendril
* Anti-Air Ability: Anchor, prevent movement
* Secondary Ability: Attack (Fire)
* Tertiary Ability: Create Tendril (Water)
* Tendrils: many, slow, persistent

Earth plays a low-mana game. Lots of charges and very slow-moving tendrils give it powerful static map control, but very little mana left over to actually _change_ the game state. Opponents have to take time eating through the earth mage's tendrils and charges in order to actually affect them -- charged shields and tendril volcanos are powerful weapons if you can get another element to help you manipulate them.

Earth hates movement effects, and has lots of ways to lock you down in your space or punish you after moving.

For patterns, earth avoids diagonals; blocky L shapes (no knight moves, even) make earth happy.

## Neutral

Neutral spells are just straight worse than others, almost always requiring an extra mana for the same (or even a worse) effect. On the other hand, they have no symbol requirement, and no particular ability weakness. A three-mana neutral spell might do damage, or give you a bunch of movement, or whatever.

For patterns, neutral takes on the desire of the elements its copying. (The primary one-mana neutral spell without a pattern just drops a tendril in your current location.)

## Elemental Pairs

- Fire / Air is a quick-moving mage that shoots fireballs, but they're a glass cannon that has to re-target with each attack.
- Air / Water is a flexible, hard-to-predict mage that can send out a bunch of chaff to hide their intentions, but they're poor at reacting quickly.
- Water / Earth is a slow-moving "tower mage" that might only cast one actual spell a turn, but affects the whole map with their permanent-power, wave-like tendrils.
- Earth / Fire is a tank with a flamethrower, prepared to deal with nearby threats but unable to affect the distant map.

## FAQs

* Attack _n_
	* Attack all creatures in target location for _n_ damage.
* Defend _n_
	* When charged, absorbs all damage from attack
	* Remove charge when it absorbs _n_ or more damage in a single attack
* Move _n_ spaces
	* Move up to _n_ spaces.
	* Terrain costs are ignored. Barriers (like Rivers or magical ones) still apply
* Place tendril
	* Optionally place a tendril in your current location. The tendril marker must come from your available mana pool
* Move tendril _n_ spaces
	* Optionally move a tendril up to _n_ spaces.
	* Tendril movement ignores all terrain costs and physical barriers
* Remove or Consume tendril
	* Remove tendril from map and place marker in spent pool
* Adjacent to Water
	* In a location adjacent to a River or adjacent to a body of water (like a Lake)
