import unreal


def create_job(sequence_path: str, map_path, render_path, config_path):

    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    queue = subsystem.get_queue()

    job = queue.allocate_new_job(unreal.MoviePipelineExecutorJob)

    # MAP
    if map_path is None:
        world = unreal.EditorLevelLibrary.get_editor_world()
        job.map = unreal.SoftObjectPath(world.get_path_name())
    else:
        job.map = unreal.SoftObjectPath(map_path)

    # SEQUENCE
    job.sequence = unreal.SoftObjectPath(sequence_path)

    # APPLY MRQ PRESET
    mrq_config = unreal.load_asset(config_path)
    job.set_configuration(mrq_config)

    # OVERRIDE OUTPUT DIRECTORY FROM ARG
    config = job.get_configuration()
    output = config.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
    output.output_directory = unreal.DirectoryPath(render_path)

    print('Sequence Added!')
    return job


def _on_mrq_finished(executor, success):

    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    queue = subsystem.get_queue()
    queue.delete_all_jobs()
    unreal.log(f"MRQ finished (success={success}). Queue cleared.")


def render_sequence():

    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)

    executor = unreal.MoviePipelinePIEExecutor(subsystem)

    executor.on_executor_finished_delegate.add_callable(_on_mrq_finished)

    subsystem.render_queue_with_executor_instance(executor)

    unreal.log(f"Started MRQ render with executor: {executor}")
    return executor


def main():

    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    queue = subsystem.get_queue()
    queue.delete_all_jobs()

    create_job(
        sequence_path='',   # e.g. '/Game/Cinematics/MySeq.MySeq'
        map_path=None,      # e.g. '/Game/Maps/MyMap.MyMap' or None to use current level
        render_path='',     # e.g. 'C:/renders/output/'
        config_path=''      # e.g. '/Game/MRQ/Presets/MyPreset.MyPreset'
    )

    render_sequence()


if __name__ == '__main__':
    main()
