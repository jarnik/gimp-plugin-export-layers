#-------------------------------------------------------------------------------
#
# This file is part of Export Layers.
#
# Copyright (C) 2013, 2014 khalim19 <khalim19@gmail.com>
#
# Export Layers is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Export Layers is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Export Layers.  If not, see <http://www.gnu.org/licenses/>.
#
#-------------------------------------------------------------------------------

"""
This module defines the plug-in settings.
"""

#===============================================================================

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

str = unicode

#===============================================================================

from collections import OrderedDict

import gimp
import gimpenums

from export_layers.pygimplib import pgsetting
from export_layers.pygimplib import pgsettinggroup
from export_layers.pygimplib import pgpath
from export_layers import exportlayers

#===============================================================================


def create_special_settings():
  """
  Create "special" plug-in settings.
  
  These settings require special handling in the code, hence their separation
  from the other settings.
  """
  
  return pgsettinggroup.SettingGroup([
    {
      'type': pgsetting.SettingTypes.enumerated,
      'name': 'run_mode',
      'default_value': 'non_interactive',
      'options': [('interactive', "RUN-INTERACTIVE", gimpenums.RUN_INTERACTIVE),
                  ('non_interactive', "RUN-NONINTERACTIVE", gimpenums.RUN_NONINTERACTIVE),
                  ('run_with_last_vals', "RUN-WITH-LAST-VALS", gimpenums.RUN_WITH_LAST_VALS)],
      'display_name': _("The run mode")
    },
    {
      'type': pgsetting.SettingTypes.image,
      'name': 'image',
      'default_value': None,
      'validate_default_value': False,
      'display_name': _("Image")
    },
    {
      'type': pgsetting.SettingTypes.boolean,
      'name': 'first_run',
      'default_value': True,
      'pdb_registration_mode': pgsetting.PdbRegistrationModes.not_registrable,
      'description': _(
        "True if the plug-in successfully ran for the first time "
        "in one GIMP session, False for subsequent runs."
      )
    },
  ])


#===============================================================================


def create_main_settings():
  file_extension_display_name = _("File extension")
  file_ext_mode_options = OrderedDict(
    [('no_special_handling', _("No special handling")),
     ('only_matching_file_extension', _("Export only layers matching file extension")),
     ('use_as_file_extensions', _("Use as file extensions"))]
  )
  square_bracketed_mode_options = OrderedDict(
    [('normal', _("Treat as normal layers")),
     ('background', _("Treat as background layers")),
     ('ignore', _("Ignore")),
     ('ignore_other', _("Ignore other layers"))]
  )
  
  main_settings = pgsettinggroup.SettingGroup([
    {
      'type': pgsetting.SettingTypes.file_extension,
      'name': 'file_extension',
      'default_value': "png",
      'display_name': file_extension_display_name,
      'description': _(
        "Type in file extension (with or without the leading period). "
        "To export in RAW format, type \"data\"."
      )
    },
    {
      'type': pgsetting.SettingTypes.directory,
      'name': 'output_directory',
      'default_value': gimp.user_directory(1),   # "Documents" directory
      'display_name': _("Output directory")
    },
    {
      'type': pgsetting.SettingTypes.boolean,
      'name': 'layer_groups_as_folders',
      'default_value': False,
      'display_name': _("Treat layer groups as folders"),
      'description': _(
        "If enabled, layers will be exported to subfolders corresponding to the layer groups.\n"
        "If disabled, all layers will be exported to the output folder on the same level."
      )
    },
    {
      'type': pgsetting.SettingTypes.boolean,
      'name': 'ignore_invisible',
      'default_value': False,
      'display_name': _("Ignore invisible layers"),
      'description': _(
        "If enabled, invisible layers will not be exported. Visible layers within "
        "invisible layer groups will also not be exported."
      )
    },
    {
      'type': pgsetting.SettingTypes.boolean,
      'name': 'autocrop',
      'default_value': False,
      'display_name': _("Autocrop layers"),
      'description': _(
        "If enabled, layers will be autocropped before being exported."
      )
    },
    {
      'type': pgsetting.SettingTypes.boolean,
      'name': 'use_image_size',
      'default_value': False,
      'display_name': _("Use image size"),
      'description': _(
        "If enabled, layers will be resized (but not scaled) to the image size. This is "
        "useful if you want to keep the size of the image canvas and the layer position "
        "within the image. If layers are partially outside the image canvas, "
        "they will be cut off."
      )
    },
    {
      'type': pgsetting.SettingTypes.enumerated,
      'name': 'file_ext_mode',
      'default_value': 'no_special_handling',
      'options': file_ext_mode_options.items(),
      'display_name': _("File extensions in layer names"),
      'description': _(
        'If "{0}" is selected, "{1}" must still be '
        'specified (for layers with invalid or no file extension).'
      ).format(file_ext_mode_options['use_as_file_extensions'], file_extension_display_name)
    },
    {
      'type': pgsetting.SettingTypes.enumerated,
      'name': 'strip_mode',
      'default_value': 'identical',
      'options': [('always', _("Always strip file extension")),
                  ('identical', _("Strip identical file extension")),
                  ('never', _("Never strip file extension"))],
      'display_name': _("File extension stripping"),
      'description': _(
        "Determines when to strip file extensions from layer names (including the period)."
      )
    },
    {
      'type': pgsetting.SettingTypes.enumerated,
      'name': 'square_bracketed_mode',
      'default_value': 'normal',
      'options': square_bracketed_mode_options.items(),
      'display_name': _("Layer names in [square brackets]"),
      'description': _(
        '"{0}": these layers will be used as a background for all other layers '
        'and will not be exported separately.\n'
        '"{1}": these layers will not be exported (and will not be treated as '
        'background layers).\n'
        '"{2}": all other layers will not be exported.'
      ).format(square_bracketed_mode_options['background'],
               square_bracketed_mode_options['ignore'],
               square_bracketed_mode_options['ignore_other'])
    },
    {
      'type': pgsetting.SettingTypes.boolean,
      'name': 'crop_to_background',
      'default_value': False,
      'display_name': _("Crop to background"),
      'description': _(
        "If enabled, layers will be cropped to the combined size of the "
        "background layers instead of their own size."
      )
    },
    {
      'type': pgsetting.SettingTypes.boolean,
      'name': 'merge_layer_groups',
      'default_value': False,
      'display_name': _("Merge layer groups"),
      'description': _(
        "If enabled, each top-level layer group is merged into one layer. The name "
        "of each merged layer is the name of the corresponding top-level layer group."
      )
    },
    {
      'type': pgsetting.SettingTypes.boolean,
      'name': 'empty_folders',
      'default_value': False,
      'display_name': _("Create folders for empty layer groups"),
      'description': _(
        "If enabled, subfolders for empty layer groups will be created."
      )
    },
    {
      'type': pgsetting.SettingTypes.boolean,
      'name': 'ignore_layer_modes',
      'default_value': False,
      'display_name': _("Ignore layer modes"),
      'description': _(
        "If enabled, the layer mode for each layer will be set to Normal. This is "
        "useful for layers with opacity less than 100% and a layer mode different "
        "than Normal or Dissolve, which would normally be completely invisible "
        "if a file format supporting alpha channel is used (such as PNG)."
      )
    },
    {
      'type': pgsetting.SettingTypes.enumerated,
      'name': 'overwrite_mode',
      'default_value': 'rename_new',
      'options': [('replace', _("Replace"), exportlayers.OverwriteHandler.REPLACE),
                  ('skip', _("Skip"), exportlayers.OverwriteHandler.SKIP),
                  ('rename_new', _("Rename new file"), exportlayers.OverwriteHandler.RENAME_NEW),
                  ('rename_existing', _("Rename existing file"), exportlayers.OverwriteHandler.RENAME_EXISTING),
                  ('cancel', _("Cancel"), exportlayers.OverwriteHandler.CANCEL)],
      'display_name': _("Overwrite mode (non-interactive run mode only)"),
      'description': _(
        "Indicates how to handle conflicting files. Skipped layers "
        "will not be regarded as exported."
      )
    },
  ])
  
  #-----------------------------------------------------------------------------
  
  main_settings['file_extension'].error_messages['default_needed'] = _(
    "You need to specify default file extension for layers with invalid or no extension."
  )
  
  #-----------------------------------------------------------------------------
  
  def streamline_layer_groups_as_folders(layer_groups_as_folders, empty_folders, merge_layer_groups):
    if not layer_groups_as_folders.value:
      empty_folders.set_value(False)
      empty_folders.ui_enabled = False
      merge_layer_groups.ui_enabled = True
    else:
      empty_folders.ui_enabled = True
      merge_layer_groups.ui_enabled = False
      merge_layer_groups.set_value(False)
  
  def streamline_file_ext_mode(file_ext_mode, file_extension, strip_mode):
    if file_ext_mode.value == file_ext_mode.options['no_special_handling']:
      strip_mode.ui_enabled = True
      file_extension.error_messages[pgpath.FileExtensionValidator.IS_EMPTY] = ""
    elif file_ext_mode.value == file_ext_mode.options['only_matching_file_extension']:
      strip_mode.set_value(strip_mode.options['never'])
      strip_mode.ui_enabled = False
      file_extension.error_messages[pgpath.FileExtensionValidator.IS_EMPTY] = ""
    elif file_ext_mode.value == file_ext_mode.options['use_as_file_extensions']:
      strip_mode.set_value(strip_mode.options['never'])
      strip_mode.ui_enabled = False
      file_extension.error_messages[pgpath.FileExtensionValidator.IS_EMPTY] = (
        file_extension.error_messages['default_needed']
      )
  
  def streamline_merge_layer_groups(merge_layer_groups, layer_groups_as_folders):
    if merge_layer_groups.value:
      layer_groups_as_folders.set_value(False)
      layer_groups_as_folders.ui_enabled = False
    else:
      layer_groups_as_folders.ui_enabled = True
  
  def streamline_autocrop(autocrop, square_bracketed_mode, crop_to_background):
    if autocrop.value and square_bracketed_mode.value == square_bracketed_mode.options['background']:
      crop_to_background.ui_enabled = True
    else:
      crop_to_background.set_value(False)
      crop_to_background.ui_enabled = False
  
  def streamline_square_bracketed_mode(square_bracketed_mode, autocrop, crop_to_background):
    if autocrop.value and square_bracketed_mode.value == square_bracketed_mode.options['background']:
      crop_to_background.ui_enabled = True
    else:
      crop_to_background.set_value(False)
      crop_to_background.ui_enabled = False
  
  #-----------------------------------------------------------------------------
  
  main_settings['layer_groups_as_folders'].set_streamline_func(
    streamline_layer_groups_as_folders, main_settings['empty_folders'], main_settings['merge_layer_groups']
  )
  main_settings['file_ext_mode'].set_streamline_func(
    streamline_file_ext_mode, main_settings['file_extension'], main_settings['strip_mode']
  )
  main_settings['merge_layer_groups'].set_streamline_func(
    streamline_merge_layer_groups, main_settings['layer_groups_as_folders']
  )
  main_settings['autocrop'].set_streamline_func(
    streamline_autocrop, main_settings['square_bracketed_mode'], main_settings['crop_to_background']
  )
  main_settings['square_bracketed_mode'].set_streamline_func(
    streamline_square_bracketed_mode, main_settings['autocrop'], main_settings['crop_to_background']
  )
  
  #-----------------------------------------------------------------------------
  
  return main_settings


#===============================================================================


def create_gui_settings():
  return pgsettinggroup.SettingGroup([
    {
      'type': pgsetting.SettingTypes.generic,
      'name': 'dialog_position',
      'default_value': (),
      'resettable_by_group': False
    },
    {
      'type': pgsetting.SettingTypes.boolean,
      'name': 'advanced_settings_expanded',
      'default_value': False,
      'resettable_by_group': False
    },
  ])


def create_session_only_gui_settings():
  return pgsettinggroup.SettingGroup([
    {
      'type': pgsetting.SettingTypes.generic,
      'name': 'image_ids_and_folders',
      'default_value': {},
      'resettable_by_group': False
    },
  ])

