<?php

namespace Deployer;

use Deployer\Exception\Exception;
use function Deployer\Support\str_contains;

require 'recipe/common.php';

set('application', 'animalistic:api');
set('repository', 'https://github.com/titomiguelcosta/animalistic-api.git');
set('git_tty', false);
set('keep_releases', 3);
set('shared_dirs', ['public/media']);
set('writable_dirs', ['']);
set('writable_mode', 'acl');

host('pi')
    ->user('pi')
    ->stage('dev')
    ->set('deploy_path', '/home/pi/animalistic/api')
    ->set('shared_files', ['.env', 'db.sqlite3'])
    ->set('branch', 'main')
    ->set('env', ['PATH' => '/home/pi/.pyenv/plugins/pyenv-virtualenv/shims:/home/pi/.pyenv/shims:/home/pi/.pyenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin']);

task('workers:restart', function () {
    run('sudo supervisorctl reload');
});

task('database:migrate', function () {
    run('python {{release_path}}/manage.py migrate --noinput');
});

task('publish:assets', function () {
    run('python {{release_path}}/manage.py collectstatic --noinput');
});

task('update:dependencies', function () {
    run('pip install -r {{release_path}}/requirements.txt', ['timeout' => null]);
});

desc('Deploy project');
task('deploy', [
    'deploy:info',
    'deploy:setup',
    'deploy:lock',
    'deploy:release',
    'deploy:update_code',
    'update:dependencies',
    'deploy:shared',
    'deploy:writable',
    'database:migrate',
    'publish:assets',
    'deploy:symlink',
    'workers:restart',
    'deploy:unlock',
    'deploy:cleanup',
    'success',
]);

after('deploy:failed', 'deploy:unlock');

desc('Preparing host for deploy');
task('deploy:setup', function () {
    // Check if shell is POSIX-compliant
    $result = run('echo $0');

    if (!str_contains($result, 'bash') && !str_contains($result, 'sh')) {
        throw new \RuntimeException(
            'Shell on your server is not POSIX-compliant. Please change to sh, bash or similar.'
        );
    }

    run('if [ ! -d {{deploy_path}} ]; then mkdir -p {{deploy_path}}; fi');

    // Check for existing /current directory (not symlink)
    $result = test('[ ! -L {{deploy_path}}/current ] && [ -d {{deploy_path}}/current ]');
    if ($result) {
        throw new Exception('There already is a directory (not symlink) named "current" in ' . get('deploy_path') . '. Remove this directory so it can be replaced with a symlink for atomic deployments.');
    }

    // Create metadata .dep dir.
    run("cd {{deploy_path}} && if [ ! -d .dep ]; then mkdir .dep; fi");

    // Create releases dir.
    run("cd {{deploy_path}} && if [ ! -d releases ]; then mkdir releases; fi");

    // Create shared dir.
    run("cd {{deploy_path}} && if [ ! -d shared ]; then mkdir shared; fi");
});

desc('Cleaning up old releases');
task('deploy:cleanup', function () {
    $releases = get('releases_list');
    $keep = get('keep_releases');
    $runOpts = [];

    if ($keep === -1) {
        // Keep unlimited releases.
        return;
    }

    while ($keep > 0) {
        array_shift($releases);
        --$keep;
    }

    foreach ($releases as $release) {
        run("rm -rf {{deploy_path}}/releases/$release", $runOpts);
    }

    run("cd {{deploy_path}} && if [ -e release ]; then rm release; fi", $runOpts);
});
