import unreal
# import numpy as np
import random


asset_name = 'asset'
pts_list = []
num_cameras = 5000


def cameras_creator():

    camera_list = []
    for cameras in range(num_cameras):

        if random.random() > 0.5:
            random_x = random.uniform(-1900, 1900)
            random_y = random.uniform(-1300, 1300)
            random_z = random.uniform(0, 800)
        else:
            random_x = random.uniform(-1900, 1900)
            random_y = random.uniform(-2200, 2200)
            random_z = random.uniform(800, 1500)

        rot_x = 0
        rot_y = random.uniform(0, 360)
        rot_z = random.uniform(-45, 45)

        camera_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.CineCameraActor,
            unreal.Vector(random_x, random_y, random_z),
            unreal.Rotator(rot_x, rot_y, rot_z)
        )

        camera_name = f"Camera_{cameras + 1}"
        camera_actor.set_actor_label(camera_name)

        # Optional: Look-at tracking (set actor_to_track first)
        # actor_to_track = unreal.EditorLevelLibrary.get_selected_level_actors()[0]
        # _lookAtSettings = unreal.CameraLookatTrackingSettings()
        # _lookAtSettings.actor_to_track = actor_to_track
        # _lookAtSettings.allow_roll = True
        # _lookAtSettings.enable_look_at_tracking = True
        # _lookAtSettings.relative_offset = unreal.Vector(0.0, 0.0, 100.0)
        # camera_actor.lookat_tracking_settings = _lookAtSettings

        camera_component = camera_actor.get_cine_camera_component()

        filmback = camera_component.get_editor_property("filmback")
        filmback.set_editor_property("sensor_height", 13.365)
        filmback.set_editor_property("sensor_width", 23.76)

        lens_settings = camera_component.get_editor_property("lens_settings")
        lens_settings.set_editor_property("min_focal_length", 12.0)
        lens_settings.set_editor_property("max_focal_length", 12.0)
        lens_settings.set_editor_property("min_f_stop", 2.8)
        lens_settings.set_editor_property("max_f_stop", 22)

        camera_component.set_editor_property("current_focal_length", 12.0)
        camera_component.set_editor_property("current_aperture", 2.8)

        camera_list.append(camera_actor)

    return camera_list


def create_level_sequence(asset_name='1', package_path='/Game/SequencesCreate/', length_seconds=1/30):

    camera_list = cameras_creator()
    assert len(camera_list) == num_cameras, "Number of cameras mismatch"

    shot_start = 0
    shot_len = length_seconds / num_cameras

    for idx in range(1, num_cameras + 1):

        level_sequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
        world = unreal.EditorLevelLibrary.get_editor_world()

        # Optional: MetaHuman Control Rig (you MUST bind a SkeletalMeshActor to the sequence first)
        # rig = unreal.load_asset("/Game/Metahumans/Common/Common/MetaHuman_ControlRig.MetaHuman_ControlRig")
        # rig_class = rig.get_control_rig_class()
        # skeletal_actor = ...  # pick your actor, then add possessable and add ControlRig track

        level_actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        get_all_actors = unreal.EditorFilterLibrary.by_class(
            level_actors.get_all_level_actors(),
            unreal.CineCameraActor
        )

        camera = camera_list[idx - 1]

        rot = camera.get_actor_rotation()
        loc = camera.get_actor_location()

        rotation_pitch = rot.pitch
        rotation_yaw = rot.yaw
        rotation_roll = rot.roll

        trans_x = loc.x
        trans_y = loc.y
        trans_z = loc.z

        subsequence_asset_name = f'{asset_name}_{idx}'
        subsequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            subsequence_asset_name,
            package_path,
            unreal.LevelSequence,
            unreal.LevelSequenceFactoryNew()
        )

        camera_cut_track = subsequence.add_track(unreal.MovieSceneCameraCutTrack)
        camera_cut_section = camera_cut_track.add_section()
        camera_cut_section.set_start_frame(0)
        camera_cut_section.set_end_frame(1)

        binding = subsequence.add_possessable(camera)

        transform_track = binding.add_track(unreal.MovieScene3DTransformTrack)
        transform_section = transform_track.add_section()
        transform_section.set_start_frame(0)
        transform_section.set_end_frame(1)

        channels = transform_section.get_all_channels()

        tx_channel = channels[0]
        ty_channel = channels[1]
        tz_channel = channels[2]

        rx_channel = channels[3]  # Pitch (X)
        ry_channel = channels[4]  # Yaw (Y)
        rz_channel = channels[5]  # Roll (Z)

        for idx2 in range(1):
            tx_channel.add_key(time=unreal.FrameNumber(idx2), new_value=trans_x)
            ty_channel.add_key(time=unreal.FrameNumber(idx2), new_value=trans_y)
            tz_channel.add_key(time=unreal.FrameNumber(idx2), new_value=trans_z)

            rx_channel.add_key(time=unreal.FrameNumber(idx2), new_value=rotation_pitch)
            ry_channel.add_key(time=unreal.FrameNumber(idx2), new_value=rotation_yaw)
            rz_channel.add_key(time=unreal.FrameNumber(idx2), new_value=rotation_roll)

        camera_binding_id = unreal.MovieSceneObjectBindingID()
        camera_binding_id.set_editor_property("Guid", binding.get_id())
        camera_cut_section.set_editor_property("CameraBindingID", camera_binding_id)

    print('Sequences Created!')


def main():
    create_level_sequence()


if __name__ == '__main__':
    main()
