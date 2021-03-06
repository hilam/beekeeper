
def load_task_configs(config):
    task_data = []
    for phase, phase_configs in enumerate(config):
        for phase_name, phase_config in phase_configs.items():
            if 'subtasks' in phase_config:
                for task_configs in phase_config['subtasks']:
                    for task_name, task_config in task_configs.items():
                        # If an image is provided at the subtask level,
                        # use it; otherwise use the phase's task definition.
                        image = None
                        if task_config:
                            image = task_config.get('image', None)
                            if image is None:
                                # Backwards compatibility - look for a
                                # 'task' instead of 'image';
                                # if it exists, prepend 'beekeeper/'
                                try:
                                    image = 'beekeeper/' + task_config['task']
                                except KeyError:
                                    image = None
                        if image is None:
                            image = phase_config.get('image', None)
                            if image is None:
                                # Backwards compatibility - look for a
                                # 'task' instead of 'image';
                                # if it exists, prepend 'beekeeper/'
                                try:
                                    image = 'beekeeper/' + phase_config['task']
                                except KeyError:
                                    image = None
                        if image is None:
                            raise ValueError("Subtask %s in phase %s task %s doesn't contain a task image." % (
                                task_name, phase, phase_name
                            ))

                        # The environment is the phase environment, overridden
                        # by the task environment.
                        task_env = phase_config.get('environment', {}).copy()
                        if task_config:
                            task_env.update(task_config.get('environment', {}))
                            task_profile = task_config.get('profile', phase_config.get('profile', 'default'))

                            full_name = task_config.get('name', task_name)
                        else:
                            full_name = task_name
                            task_profile = 'default'

                        task_data.append({
                            'name': full_name,
                            'slug': "%s:%s" % (phase_name, task_name),
                            'phase': phase,
                            'is_critical': task_config.get('critical', True),
                            'environment': task_env,
                            'profile_slug': task_profile,
                            'image': image,
                        })
            elif 'image' in phase_config:
                task_data.append({
                    'name': phase_config.get('name', phase_name),
                    'slug': phase_name,
                    'phase': phase,
                    'is_critical': phase_config.get('critical', True),
                    'environment': phase_config.get('environment', {}),
                    'profile_slug': phase_config.get('profile', 'default'),
                    'image': phase_config['image'],
                })
            elif 'task' in phase_config:
                # Backward compatibility - look for a
                # 'task' instead of 'image'; if it exists, prepend 'beekeeper/'
                task_data.append({
                    'name': phase_config.get('name', phase_name),
                    'slug': phase_name,
                    'phase': phase,
                    'is_critical': phase_config.get('critical', True),
                    'environment': phase_config.get('environment', {}),
                    'profile_slug': phase_config.get('profile', 'default'),
                    'image': 'beekeeper/' + phase_config['task'],
                })
            else:
                raise ValueError("Phase %s task %s doesn't contain a task or subtask image." % (
                    phase, phase_name
                ))
    return task_data
