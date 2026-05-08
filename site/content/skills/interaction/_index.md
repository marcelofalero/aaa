+++
title = "Interaction"
attribute = "PER"
category = "Social"
type = "skill"
layout = "list"
+++

Interaction provides a character with the basics of interpersonal contact with members of the same species and native culture. Through the use of the associated specialty skills, a character can become an expert in the arts of interaction and communication. 

While everyone who grows up around other people has some skill at interacting with others, those who purchase any of the specialty skills are either trained or naturally proficient at winning friends and influencing people. 

### Specialties
Interaction includes specific areas such as:
<<<<<<< HEAD
- [Bargain](#bargain)
- [Charm](#charm)
- [Interview](#interview)
- [Intimidate](#intimidate)
- [Seduce](#seduce)
- [Taunt](#taunt)
=======
- [Bargain]({{< relref "bargain" >}})
- [Charm]({{< relref "charm" >}})
- [Interview]({{< relref "interview" >}})
- [Intimidate]({{< relref "intimidate" >}})
- [Seduce]({{< relref "seduce" >}})
- [Taunt]({{< relref "taunt" >}})
>>>>>>> origin/main

### Interaction Situation Modifiers

| Relation / Condition | Modifier |
| :---  | :--- |
| Target is different species | +2 steps |
| Target is different culture | +2 steps |
| Strangers | +1 step |
| Known to each other | 0 |
| Acquainted | -1 step |

### Mechanics
<<<<<<< HEAD
Interaction is an **encounter skill**, meaning that any skill check takes into account the target's starting attitude (see [Table P25: Encounter Skill Effects]({{< relref "/core-mechanics/useful-tables#table-p25-encounter-skill-effects" >}})). 
=======
Interaction is an **encounter skill**, meaning that any skill check takes into account the target's starting attitude (see [Table P25: Encounter Skill Effects]({{< relref "core-mechanics/useful-tables#table-p25-encounter-skill-effects" >}})). 
>>>>>>> origin/main

- **Target Restrictions:** Neither a **Combative** character nor a **Fanatic** character can be influenced by Interaction.
- **Resistance:** The target's **Will resistance modifier** also applies. 
- **Cumulative Modifiers:** The modifiers listed above are cumulative. 
- **Longevity:** In general, the changes in attitude that can be brought about by the use of Interaction are longer-lasting than the changes achieved through the use of Deception or Entertainment skills. Otherwise, a target’s change in attitude lasts until the character does something to alter that attitude in either a positive or negative way. 

> When possible, it's better to roleplay an Interaction encounter than simply rolling dice and deciding an outcome.

## Bargain
{{< specialty attr="PER" untrained="yes" cost="3" >}}

Bargain represents a character’s ability to negotiate a cheaper price for an object they want to buy or a better price for one they’re selling. It also covers more formal business negotiations. A successful check improves the character’s position at the bargaining table. 

The degree of success determines who gets the better outcome. A success also changes the target’s attitude as shown on [Table P25: Encounter Skill Effects]({{< relref "core-mechanics/useful-tables#table-p25-encounter-skill-effects" >}}).

### Bargain Situation Modifiers

| Condition | Modifier |
| :--- | :--- |
| **Opponent Attitude** | |
| Hostile | +2 steps |
| Neutral | 0 |
| Friendly | -2 steps |
| **Opponent Training** | |
| Opponent has no ranks in bargain | -2 steps |
| Opponent has ranks in bargain | 0 |
| **Supply** | |
| Supply is low | +2 steps |
| Supply is moderate | 0 |
| Supply is high | -1 step |
| **Demand** | |
| Demand is low | -2 steps |
| Demand is moderate | 0 |
| Demand is high | +2 steps |

> [!IMPORTANT]
> Bargain can be used on targets of any attitude **except** **Fanatic** or **Combative**.

---

## Charm
{{< specialty attr="PER" untrained="yes" cost="3" >}}

The charm skill represents a character’s ability to change the attitudes of those they interact with by presenting themselves in a likable, friendly manner. A character with this skill seeks to charm others into giving up something—whether it’s material goods or simply a change of attitude—with kind words, a winning smile, and a personable attitude. 

To actually charm someone, the character must achieve an **Ordinary** result or better. The result of the check determines how much the target’s attitude improves, as shown on [Table P25: Encounter Skill Effects]({{< relref "core-mechanics/useful-tables#table-p25-encounter-skill-effects" >}}).

> [!IMPORTANT]
> Charm can only be used on targets whose attitude is **Neutral** or **Friendly**. A character cannot charm a **Hostile** or **Combative** target. A character might need to use **Bargain**, **Interview**, or **Intimidate** to change a character's attitude to Neutral before attempting to use Charm.

---

## Interview
{{< specialty attr="PER" untrained="yes" cost="3" >}}

The interview skill represents a character’s ability to get information from another character in a non-aggressive way. Interviews are often used by reporters, investigators, and officials conducting standard administrative procedures. It differs from **Investigate—interrogate** (a **Will**-based skill) in the amount of aggressiveness and fear applied by the questioner. 

The result of the check determines the amount of information the character is able to obtain. A success also changes the target’s attitude as shown on [Table P25: Encounter Skill Effects]({{< relref "core-mechanics/useful-tables#table-p25-encounter-skill-effects" >}}).

> [!IMPORTANT]
> Interview can only be used on targets whose attitude is **Neutral**, **Friendly**, or better. A character cannot interview a **Hostile** or **Combative** target. A character might need to use **Intimidate** or **Bargain** to change a character's attitude to Neutral before attempting an interview.

---

## Intimidate
{{< specialty attr="PER" untrained="yes" cost="3" >}}

The intimidate skill represents a character’s ability to threaten another, either by physical presence or the weight of authority. Intimidate enables a character to force an opponent to back down, reveal information, or cooperate in some other way due to fear. 

The target's **Will resistance modifier** applies to the skill check, along with other Interaction modifiers. The greater the degree of success, the more cooperation the character can elicit. A success also changes the target's attitude as shown on [Table P25: Encounter Skill Effects]({{< relref "core-mechanics/useful-tables#table-p25-encounter-skill-effects" >}}).

> [!IMPORTANT]
> Intimidate can be used on targets of any attitude **except** **Fanatic** or **Combative**. A character can be intimidated into having a Neutral or even a Friendly attitude, depending on the result of the skill check.

---

## Seduce
{{< specialty attr="PER" untrained="yes" cost="3" >}}

The seduce skill represents the ability to entice or beguile another character through the use of opening lines, witty exchanges, playful conversation, and intimate behavior. To seduce another character is to manipulate that character’s emotions through planned exchanges. 

The final goal of seduction is to gain the seduced character's trust or cooperation through romantic overtures. To actually accomplish the seduction, the character must achieve an **Ordinary** result or better. 

### Seduction Effects
A seduced character won't stay that way forever. How long the character remains seduced depends on the result of the check:
- **Charmed**: The seduction works well enough to lead to serious feelings that will last if the seducer continues to feign interest (requires a successful seduce skill check at least once per week).
- **Fanatic**: The seduction works so well that the target falls in love with (or becomes obsessed with) the seducer.

### Asking for Favors
Every time the seducer asks for a favor of any sort, the seduced character makes a **Will feat check** with a modifier based on their attitude:
- **Charmed**: +1 penalty
- **Fanatic**: +2 penalty

A success on this feat check indicates that the seduced character’s attitude is altered by one grade toward Neutral (Fanatic to Charmed, or Charmed to Friendly). Once the seduced character's attitude shifts to Friendly, they no longer behave as though seduced.

> [!IMPORTANT]
> Seduce can only be used on targets whose attitude is **Friendly** or better. A character cannot seduce a target whose attitude is **Neutral**, **Hostile**, or **Combative**. A character might need to use **Charm** to improve a target's attitude to Friendly before attempting to seduce them.

---

## Taunt
{{< specialty attr="PER" untrained="yes" cost="3" >}}

Taunt represents a character''s ability to trade insults in order to rattle or enrage an opponent. A character who taunts his opponent tries to force him into making an error in judgment.

### Taunt Situation Modifiers

| Target Attitude | Modifier |
| :--- | :--- |
| Combative | -2 steps |
| Hostile | -1 step |
| Neutral | 0 |
| Friendly | +1 step |

- On an **Ordinary** success, the taunt is effective, providing a **+1 penalty** to the target''s next action.
- On a **Good** success, the penalty is **+2**
- On an **Amazing** success, the penalty is **+3**.

Success also enrages the target and shifts their attitude toward **Combative** (Neutral to Hostile, for example). After a Critical Failure or a Failure result, a character can make another attempt to taunt someone else. However, only one successful taunt can be directed at a target in a scene.

---

