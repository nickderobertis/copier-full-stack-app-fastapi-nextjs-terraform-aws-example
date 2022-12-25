# Infrastructure

## Setup

Ensure `direnv` is installed and run `direnv allow`. It will create a `.env` file with
values to fill out.

### Global Environment

The global environment is not managed by CI/CD, it must be manually created and updated.
cd into `global` and run `terragrunt init` and `terragrunt apply`.

### Monitoring

#### Slack Alerts

To set up Slack alerting, you need a Slack Workspace and then to create an app
connected to that workspace. [Create the app](https://api.slack.com/apps) with the following manifest:

```yaml
_metadata:
  major_version: 1
  minor_version: 1
display_information:
  name: App Example Monitoring
  description: App Example System Monitoring
  background_color: "#d982b5"
features:
  bot_user:
    display_name: MonitorBot
    always_online: true
  app_home:
    home_tab_enabled: false
    messages_tab_enabled: true
    messages_tab_read_only_enabled: true
oauth_config:
  scopes:
    user:
      - channels:write
      - channels:read
      - chat:write
      - files:write
    bot:
      - channels:history
      - channels:join
      - channels:manage
      - channels:read
      - chat:write.customize
      - chat:write.public
      - chat:write
      - files:write
settings:
  interactivity:
    is_enabled: true
  org_deploy_enabled: false
  socket_mode_enabled: true
  token_rotation_enabled: false
settings:
  interactivity:
    is_enabled: true
  org_deploy_enabled: false
  socket_mode_enabled: true
```

Then you will need to:

1. Add the app to the workspace
2. Go to "Oauth and Permissions", copy the user token and add it to the `.env` file as `SLACK_TOKEN`
3. Add the incoming webhook app to the workspace and add the URL to the `.env` file as `SLACK_WEBHOOK_URL`

> TODO: Is step 3 necessary?

## Deployment Structure

All environments except `global` are managed via CI/CD. To deploy the `global` environment,
cd into `global` and run `terragrunt run-all apply`.

## Project Structure

One off folders:

- `settings`: Python environment variables validation
- `modules`: Terraform modules
- `common`: Terragrunt configuration shared across environments

Environments:

- `staging`
- `prod`
- `global` - Used by all other environments
- `api-preview` - For PR API previews, shares state with `infra-preview`
- `infra-preview` - For PR infrastructure previews, shares state with `api-preview`

`cd` into any of the environment folders to work on that environment.

## Deployment

Run `terragrunt run-all apply` to deploy the infrastructure.

## Maintenance

## Adding Parameters/Secrets

Edit `common/secrets.hcl` to put secrets and plain parameters into AWS SSM under the
current app and environment.

Edit `global/secrets/terragrunt.hcl` to put secrets and plain parameters into AWS SSM
in the global namespace that can be accessed by all environments.

### VPC VPN

You can put yourself on the VPC via the VPN, to be able to access the infrastructure directly.
After deploying, you can connect via `./network/connect-vpn.sh` and disconnect via `./network/disconnect-vpn.sh`.
Currently the connection scripts are only supported for [openvpn3 on Linux](https://community.openvpn.net/openvpn/wiki/OpenVPN3Linux).

## Best Practices

### Add Providers First

When adding a new provider, add it in a separate PR and merge it to main before adding
any resources that use it. This will ensure that if anything goes wrong with the final
deployment, CI will be able to roll-back to the state that has only the provider. If the
provider is added at the same time, the roll-back commit will not include the provider
and so Terraform will skip managing those resources entirely, leaving orphan resources.

## Debugging

### API

#### Exec into Container

Run `./api/exec.sh` from the `infra` folder.

## Development

Use the `infra-preview` environment to test infrastructure changes. The easiest way
is to put up a PR with some initial change in the `infra` folder. This will cause
CI to create a preview environment for you. Once it is ready, set the following
variables in `.env`, changing the PR number to match your PR:

```bash
APP_STAGING_NAME_SUFFIX=pr-13
NETWORK_STAGING_SUBDOMAIN=pr-13
```

Then cd into `infra-preview` and run `terragrunt run-all init -reconfigure --terragrunt-ignore-external-dependencies`.
From there, you are fully connected to the environment and can apply or destroy whatever you want.

If you end up getting your environment into a bad state, you can destroy it by closing the PR.
Make sure to check the action result, as it could fail and then you will need to destroy some
resources manually.
