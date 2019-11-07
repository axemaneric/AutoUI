## Gitlab CI Runner

Go to CI/CD tab on the left menu to view pipeline.

CI/CD->Environments views all current deployments.

#### Jenkins Builds
dev: https://awsjenkins.openmarket.com/view/OPS/job/OPS-gitlab-runner-dev/

stage: https://awsjenkins.openmarket.com/view/OPS/job/OPS-gitlab-runner-stage/

prod:  https://awsjenkins.openmarket.com/view/OPS/job/OPS-gitlab-runner-prod/

#### Resources
- Creates a t2.micro EC2 instance for Gitlab Runner
- Creates an S3 bucket to store tfstates

#### Usage
1. Configure the Terraform.
2. Build through Jenkins
3. Check **Settings**->**CI/CD**->**Runner Settings**. A runner should be automatically registered at instance creation.
4. Go to another project and activate runner, read CI service secion here: https://wiki.openmarket.com/display/CT/Gitlab+CI+on+AWS

#### Notes
- The gitlab runner uses a default **Docker** environment
- The Terraform here uses ansible to automatically configure and register a default runner
- This automatically registered runner is registered to this project (om-gitlab-ci), but is unlocked and free to add for all of OM's gitlab projects
- Very slow. Only one job at a time. As of 09-12-2019.

Use below if a new runner needs to be configured, otherwise, a runner is automatically registered upon instance creation

#### Configuring a Runner
```bash
# ssh into the instance
...
# To view commands
$ sudo gitlab-runner
# Register a gitlab runner with Docker executor
$ sudo gitlab-runner register
Runtime platform                                    arch=amd64 os=linux pid=14796 revision=d0b76032 version=12.0.2
Running in system-mode.

Please enter the gitlab-ci coordinator URL (e.g. https://gitlab.com/):
https://gitlab.openmarket.com/
Please enter the gitlab-ci token for this runner:
82kbRSfDSmLAmGhv7szh
Please enter the gitlab-ci description for this runner:
[ip-10-55-26-159]: example-runner
Please enter the gitlab-ci tags for this runner (comma separated):

Registering runner... succeeded                     runner=82kbRSfD
Please enter the executor: ssh, virtualbox, docker-ssh+machine, kubernetes, parallels, docker-ssh, shell, docker+machine, docker:
docker
Please enter the default Docker image (e.g. ruby:2.6):
hashicorp/terraform:light
Runner registered successfully. Feel free to start it, but if it\'s running already the config should be automatically reloaded!
# View runners
$ sudo gitlab-runner list
Runtime platform                                    arch=amd64 os=linux pid=18337 revision=d0b76032 version=12.0.2
Listing configured runners                          ConfigFile=/etc/gitlab-runner/config.toml
example-runner                                      Executor=docker Token=c25c76a8a6ceaa3cef34ae6a6162d9 URL=https://gitlab.openmarket.com/
# Check status
$ sudo gitlab-runner verify
Runtime platform                                    arch=amd64 os=linux pid=14837 revision=d0b76032 version=12.0.2
Running in system-mode.

Verifying runner... is alive                        runner=c25c76a8
```
