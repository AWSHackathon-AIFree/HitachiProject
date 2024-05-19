require 'openstudio'

# 加載現有的OSM文件
osm_path = OpenStudio::Path.new('path/to/your_model.osm')
model = OpenStudio::Model::Model.load(osm_path).get

# 獲取第一個熱區域
thermal_zone = model.getThermalZones.first

# 創建一個新的四管風機盤管系統並添加到熱區域
hvac = OpenStudio::Model::FourPipeFanCoil.new(model)
hvac.addToThermalZone(thermal_zone)

# 創建運行Schedule
cooling_schedule_experiment = OpenStudio::Model::ScheduleRuleset.new(model)
rule = OpenStudio::Model::ScheduleRule.new(cooling_schedule_experiment)
day_schedule = rule.daySchedule
day_schedule.addValue(OpenStudio::Time.new(0, 6, 0, 0), 1)
day_schedule.addValue(OpenStudio::Time.new(0, 24, 0, 0), 0)

# 添加運行Schedule到HVAC系統
hvac.setAvailabilitySchedule(cooling_schedule_experiment)

# 保存修改後的模型
model.save(OpenStudio::Path.new('path/to/modified_model.osm'), true)

# 設置模擬運行週期
simulation_control = model.getSimulationControl
simulation_control.setRunPeriod(model.getRunPeriod)
model.getRunPeriod.setBeginMonth(1)
model.getRunPeriod.setBeginDayOfMonth(1)
model.getRunPeriod.setEndMonth(12)
model.getRunPeriod.setEndDayOfMonth(31)

# 設置氣象文件
weather_file = OpenStudio::WeatherFile.setWeatherFile(model, 'path/to/weatherfile.epw')

# 保存模型
model.save(OpenStudio::Path.new('path/to/modified_model.osm'), true)

# 運行模擬
workflow = OpenStudio::WorkflowJSON.new
workflow.setSeedFile(OpenStudio::Path.new('path/to/modified_model.osm'))
workflow.setWeatherFile(weather_file)
workflow.save(OpenStudio::Path.new('path/to/workflow.osw'))

system("openstudio run -w path/to/workflow.osw")
