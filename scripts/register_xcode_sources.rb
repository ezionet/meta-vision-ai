# Run with: ruby scripts/register_xcode_sources.rb
# Requires: gem install xcodeproj
require 'xcodeproj'
project_path = 'ios/MetaVisionAI/CameraAccess.xcodeproj'
abort "Missing #{project_path}; import and commit CameraAccess first" unless File.exist?(project_path)
project = Xcodeproj::Project.open(project_path)
target = project.targets.find { |t| t.name == 'CameraAccess' }
abort 'CameraAccess app target not found' unless target
group = project.main_group.find_subpath('CameraAccess', false)
abort 'CameraAccess source group not found' unless group
%w[AnalysisClient.swift AnalysisScreen.swift].each do |name|
  path = "ios/MetaVisionAI/CameraAccess/#{name}"
  abort "Missing #{path}" unless File.file?(path)
  ref = group.files.find { |f| f.path == name } || group.new_file(name)
  phase = target.source_build_phase
  phase.add_file_reference(ref, true) unless phase.files_references.include?(ref)
end
project.save
puts 'Registered analysis Swift files in CameraAccess target'
