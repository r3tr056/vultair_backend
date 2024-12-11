var utg = 
{
  "nodes": [
    {
      "id": "5fefb8af825cf2966741a169330f8431",
      "shape": "image",
      "image": "states\\screen_2024-12-11_015514.jpg",
      "label": "NexusLauncherActivity\n<FIRST>",
      "package": "com.google.android.apps.nexuslauncher",
      "activity": ".NexusLauncherActivity",
      "state_str": "5fefb8af825cf2966741a169330f8431",
      "structure_str": "0303c0f04b6cc079ca1365e79ee56f2d",
      "title": "<table class=\"table\">\n<tr><th>package</th><td>com.google.android.apps.nexuslauncher</td></tr>\n<tr><th>activity</th><td>.NexusLauncherActivity</td></tr>\n<tr><th>state_str</th><td>5fefb8af825cf2966741a169330f8431</td></tr>\n<tr><th>structure_str</th><td>0303c0f04b6cc079ca1365e79ee56f2d</td></tr>\n</table>",
      "content": "com.google.android.apps.nexuslauncher\n.NexusLauncherActivity\n5fefb8af825cf2966741a169330f8431\ncom.google.android.apps.nexuslauncher:id/launcher,com.google.android.apps.nexuslauncher:id/workspace,com.google.android.apps.nexuslauncher:id/g_icon,android:id/content,com.google.android.apps.nexuslauncher:id/search_container_workspace,com.google.android.apps.nexuslauncher:id/scrim_view,com.google.android.apps.nexuslauncher:id/bc_smartspace_view,com.google.android.apps.nexuslauncher:id/clock,com.google.android.apps.nexuslauncher:id/drag_layer,com.google.android.apps.nexuslauncher:id/page_indicator,com.google.android.apps.nexuslauncher:id/mic_icon,com.google.android.apps.nexuslauncher:id/subtitle_text,com.google.android.apps.nexuslauncher:id/smartspace_card_pager,com.google.android.apps.nexuslauncher:id/hotseat\nMessages,Play Store,Wed, Dec 11,Chrome",
      "font": "14px Arial red"
    },
    {
      "id": "56e2e36ef5792091df2bb8b9d00434b3",
      "shape": "image",
      "image": "states\\screen_2024-12-11_015538.jpg",
      "label": "MainActivity",
      "package": "com.instagram.lite",
      "activity": "com.facebook.lite.MainActivity",
      "state_str": "56e2e36ef5792091df2bb8b9d00434b3",
      "structure_str": "2955e9bf21c83c64d4199449475fecd4",
      "title": "<table class=\"table\">\n<tr><th>package</th><td>com.instagram.lite</td></tr>\n<tr><th>activity</th><td>com.facebook.lite.MainActivity</td></tr>\n<tr><th>state_str</th><td>56e2e36ef5792091df2bb8b9d00434b3</td></tr>\n<tr><th>structure_str</th><td>2955e9bf21c83c64d4199449475fecd4</td></tr>\n</table>",
      "content": "com.instagram.lite\ncom.facebook.lite.MainActivity\n56e2e36ef5792091df2bb8b9d00434b3\ncom.instagram.lite:id/root_layout,android:id/content,android:id/navigationBarBackground,com.instagram.lite:id/main_layout,android:id/statusBarBackground\n"
    },
    {
      "id": "d9a0a967fe50d7a63f335b121a038164",
      "shape": "image",
      "image": "states\\screen_2024-12-11_015553.jpg",
      "label": "MainActivity\n<LAST>",
      "package": "com.instagram.lite",
      "activity": "com.facebook.lite.MainActivity",
      "state_str": "d9a0a967fe50d7a63f335b121a038164",
      "structure_str": "cfdeedcc251c36380a4f913c67dda486",
      "title": "<table class=\"table\">\n<tr><th>package</th><td>com.instagram.lite</td></tr>\n<tr><th>activity</th><td>com.facebook.lite.MainActivity</td></tr>\n<tr><th>state_str</th><td>d9a0a967fe50d7a63f335b121a038164</td></tr>\n<tr><th>structure_str</th><td>cfdeedcc251c36380a4f913c67dda486</td></tr>\n</table>",
      "content": "com.instagram.lite\ncom.facebook.lite.MainActivity\nd9a0a967fe50d7a63f335b121a038164\ncom.instagram.lite:id/inline_top_right_layout,com.instagram.lite:id/root_layout,com.instagram.lite:id/center_layout,com.instagram.lite:id/inline_top_left_layout,android:id/content,com.instagram.lite:id/carbon_sound_image_view,android:id/navigationBarBackground,com.instagram.lite:id/main_layout,com.instagram.lite:id/inline_bottom_left_layout,android:id/statusBarBackground,com.instagram.lite:id/video_view,com.instagram.lite:id/inline_bottom_right_layout\n",
      "font": "14px Arial red"
    }
  ],
  "edges": [
    {
      "from": "5fefb8af825cf2966741a169330f8431",
      "to": "56e2e36ef5792091df2bb8b9d00434b3",
      "id": "5fefb8af825cf2966741a169330f8431-->56e2e36ef5792091df2bb8b9d00434b3",
      "title": "<table class=\"table\">\n<tr><th>1</th><td>IntentEvent(intent='am start com.instagram.lite/com.facebook.lite.MainActivity')</td></tr>\n</table>",
      "label": "1",
      "events": [
        {
          "event_str": "IntentEvent(intent='am start com.instagram.lite/com.facebook.lite.MainActivity')",
          "event_id": 1,
          "event_type": "intent",
          "view_images": []
        }
      ]
    },
    {
      "from": "5fefb8af825cf2966741a169330f8431",
      "to": "d9a0a967fe50d7a63f335b121a038164",
      "id": "5fefb8af825cf2966741a169330f8431-->d9a0a967fe50d7a63f335b121a038164",
      "title": "<table class=\"table\">\n<tr><th>1</th><td>IntentEvent(intent='am start com.instagram.lite/com.facebook.lite.MainActivity')</td></tr>\n</table>",
      "label": "1",
      "events": [
        {
          "event_str": "IntentEvent(intent='am start com.instagram.lite/com.facebook.lite.MainActivity')",
          "event_id": 1,
          "event_type": "intent",
          "view_images": []
        }
      ]
    }
  ],
  "num_nodes": 3,
  "num_edges": 2,
  "num_effective_events": 1,
  "num_reached_activities": 1,
  "test_date": "2024-12-11 01:54:36",
  "time_spent": 80.879015,
  "num_transitions": 2,
  "device_serial": "emulator-5554",
  "device_model_number": "sdk_gphone64_x86_64",
  "device_sdk_version": 31,
  "app_sha256": "70be08e22b11324e480d325d493fecf38af66af5abd623524f16fd28b5e74aed",
  "app_package": "com.instagram.lite",
  "app_main_activity": "com.facebook.lite.MainActivity",
  "app_num_total_activities": 11
}