# Plugin marketplaces

> Create and manage plugin marketplaces to distribute Claude Code extensions across teams and communities.

Plugin marketplaces are catalogs of available plugins. Marketplaces provide centralized discovery, version management, team distribution, and flexible sources (git, GitHub, local paths).

## Marketplace structure

A marketplace requires `.claude-plugin/marketplace.json` at the marketplace root:

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@company.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    }
  ]
}
```

## Marketplace schema

### Required fields

| Field     | Type   | Description                                    |
| :-------- | :----- | :--------------------------------------------- |
| `name`    | string | Marketplace identifier (kebab-case, no spaces) |
| `owner`   | object | Marketplace maintainer information             |
| `plugins` | array  | List of available plugins                      |

### Plugin entries

**Required fields:**

| Field    | Type           | Description                               |
| :------- | :------------- | :---------------------------------------- |
| `name`   | string         | Plugin identifier (kebab-case, no spaces) |
| `source` | string\|object | Where to fetch the plugin from            |

**Optional fields:**

| Field         | Type    | Description                              |
| :------------ | :------ | :--------------------------------------- |
| `description` | string  | Brief plugin description                 |
| `version`     | string  | Plugin version                           |
| `author`      | object  | Plugin author information                |
| `strict`      | boolean | Require plugin.json in folder (default: true) |

### Plugin sources

**Relative paths** (for plugins in same repository):
```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

**GitHub repositories:**
```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

**Git repositories:**
```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

## Add and use marketplaces

```shell
# Add GitHub repository
/plugin marketplace add owner/repo

# Add git repository
/plugin marketplace add https://gitlab.com/company/plugins.git

# Add local directory
/plugin marketplace add ./my-marketplace

# Install plugin from marketplace
/plugin install plugin-name@marketplace-name
```

## Creating a marketplace

### Quick setup

1. Create `.claude-plugin/marketplace.json` in your repo root
2. Define plugin entries with sources
3. Add to Claude Code: `/plugin marketplace add owner/repo`
4. Install plugins: `/plugin install plugin-name@marketplace-name`

### Example marketplace

```json
{
  "name": "test-marketplace",
  "owner": {
    "name": "Test User"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./my-plugin",
      "description": "Test plugin",
      "version": "1.0.0",
      "author": {
        "name": "Your Name"
      }
    }
  ]
}
```
