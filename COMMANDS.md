# Commands

## `va-cli new`

Adds a new voice command

**Params:**

- `-n` `--name ""`
- `-d` `--description ""`
- `-sh` `--shell false`
- `-ph` `--phrase`
- `-cfg` `--config`

## ` va-cli update`

Updates the voice command

**Params:**

- `--id`
- `-n` `--name` New name
- `-d` `--description` New description
- `-sh` `--shell` New shell value
- `-ph` `--phrase` New phrase
- `-cfg` `--config`

## `va-cli remove`

Removes the voice command

**Params:**

- `--id`
- `-cfg` `--config`

## `va-cli find`

Finds command by id or phrase

**Params:**

- `-ph` `--phrase`
- `--id`
- `-cfg` `--config`
- `-r` `--raw` false (if true, prints raw json data)

## `va-cli reload-config`

Reloads config in current process

**Params:**

- `-cfg` `--config`

## `va-cli list`

Prints list of commands

**Params:**

- `-p` `--page` (номер страницы)
- `-cfg` `--config`
- `-r` `--raw` false (if true, prints raw json data)

## `va-cli activate`

Activates assistant

**Params:**

- `-cfg` `--config`

## `va-cli deactivate`

Deactivates assistant

**Params:**

- `-cfg` `--config`
