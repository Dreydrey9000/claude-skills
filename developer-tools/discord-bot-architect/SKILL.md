---
name: discord-bot-architect
description: "Specialized skill for building production-ready Discord bots. Covers Discord.js (JavaScript) and Pycord (Python), gateway intents, slash commands, interactive components, rate limiting, and sharding."
risk: unknown
source: "vibeship-spawner-skills (Apache 2.0)"
date_added: "2026-02-27"
---

# Discord Bot Architect

## Patterns

### Interactive Components Pattern

Using buttons, select menus, and modals for rich UX

**When to use**: ['Need interactive user interfaces', 'Collecting user input beyond slash command options', 'Building menus, confirmations, or forms']

```python
```javascript
// Discord.js - Buttons and Select Menus
const {
  SlashCommandBuilder,
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
  StringSelectMenuBuilder,
  ModalBuilder,
  TextInputBuilder,
  TextInputStyle
} = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('menu')
    .setDescription('Shows an interactive menu'),

  async execute(interaction) {
    // Button row
    const buttonRow = new ActionRowBuilder()
      .addComponents(
        new ButtonBuilder()
          .setCustomId('confirm')
          .setLabel('Confirm')
          .setStyle(ButtonStyle.Primary),
        new ButtonBuilder()
          .setCustomId('cancel')
          .setLabel('Cancel')
          .setStyle(ButtonStyle.Danger),
        new ButtonBuilder()
          .setLabel('Documentation')
          .setURL('https://discord.js.org')
          .setStyle(ButtonStyle.Link)  // Link buttons don't emit events
      );

    // Select menu row (one per row, takes all 5 slots)
    const selectRow = new ActionRowBuilder()
      .addComponents(
        new StringSelectMenuBuilder()
          .setCustomId('select-role')
          .setPlaceholder('Select a role')
          .setMinValues(1)
          .setMaxValues(3)
          .addOptions([
            { label: 'Developer', value: 'dev', emoji: '💻' },
            { label: 'Designer', value: 'design', emoji: '🎨' },
            { label: 'Community', value: 'community', emoji: '🎉' }
          ])
      );

    await interaction.reply({
      content: 'Choose an option:',
      components: [buttonRow, selectRow]
    });

    // Collect responses
    const collector = interaction.channel.createMessageComponentCollector({
      filter: i => i.user.id === interaction.user.id,
      time: 60_000  // 60 seconds timeout
    });

    collector.on('collect', async i => {
      if (i.customId === 'confirm') {
        await i.update({ content: 'Confirmed!', components: [] });
        collector.stop();
      } else if (i.custo
```

## Anti-Patterns

### ❌ Message Content for Commands

**Why bad**: Message Content Intent is privileged and deprecated for bot commands.
Slash commands are the intended approach.

### ❌ Syncing Commands on Every Start

**Why bad**: Command registration is rate limited. Global commands take up to 1 hour
to propagate. Syncing on every start wastes API calls and can hit limits.

### ❌ Blocking the Event Loop

**Why bad**: Discord gateway requires regular heartbeats. Blocking operations
cause missed heartbeats and disconnections.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | critical | ## Acknowledge immediately, process later |
| Issue | critical | ## Step 1: Enable in Developer Portal |
| Issue | high | ## Use a separate deploy script (not on startup) |
| Issue | critical | ## Never hardcode tokens |
| Issue | high | ## Generate correct invite URL |
| Issue | medium | ## Development: Use guild commands |
| Issue | medium | ## Never block the event loop |
| Issue | medium | ## Show modal immediately |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
