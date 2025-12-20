# Health Checks Database - Complete Column Mapping

## ✅ All Columns Populated from Daily Health Check

### Core Metadata
- ✅ **id** - Auto-generated primary key
- ✅ **user_id** - From session state
- ✅ **check_date** - Current date (auto)
- ✅ **check_timestamp** - Current timestamp (auto)
- ✅ **created_at** - Auto-generated
- ✅ **updated_at** - Auto-updated

### Old Schema (Backward Compatibility)
- ✅ **sit_stand_speed** → sit_stand_movement_speed
- ✅ **sit_stand_stability** → sit_stand_stability
- ✅ **walk_speed** → walk_movement_speed
- ✅ **walk_stability** → walk_stability
- ✅ **gait_symmetry** → walk_motion_smoothness
- ✅ **hand_steadiness** → steady_stability
- ✅ **tremor_index** → steady_micro_movements
- ✅ **coordination_score** → avg_stability
- ✅ **overall_mobility** → avg_movement_speed

### Sit-to-Stand Activity (8 metrics)
- ✅ **sit_stand_movement_speed** - From feature extraction
- ✅ **sit_stand_stability** - From feature extraction
- ✅ **sit_stand_motion_smoothness** - From feature extraction
- ✅ **sit_stand_posture_deviation** - From feature extraction
- ✅ **sit_stand_micro_movements** - From feature extraction
- ✅ **sit_stand_range_of_motion** - From feature extraction
- ✅ **sit_stand_acceleration_variance** - From feature extraction
- ✅ **sit_stand_frame_count** - From feature extraction

### Walking Activity (8 metrics)
- ✅ **walk_movement_speed** - From movement test
- ✅ **walk_stability** - From movement test
- ✅ **walk_motion_smoothness** - From movement test
- ✅ **walk_posture_deviation** - From movement test
- ✅ **walk_micro_movements** - From movement test
- ✅ **walk_range_of_motion** - From movement test
- ✅ **walk_acceleration_variance** - From movement test (NEWLY ADDED)
- ✅ **walk_frame_count** - From movement test

### Steady Hold Activity (8 metrics)
- ✅ **steady_movement_speed** - From stability test
- ✅ **steady_stability** - From stability test
- ✅ **steady_motion_smoothness** - From stability test
- ✅ **steady_posture_deviation** - From stability test
- ✅ **steady_micro_movements** - From stability test
- ✅ **steady_range_of_motion** - From stability test
- ✅ **steady_acceleration_variance** - From stability test (NEWLY ADDED)
- ✅ **steady_frame_count** - From stability test

### Summary Metrics (2 calculated metrics)
- ✅ **avg_movement_speed** - Calculated average
- ✅ **avg_stability** - Calculated average

## 🔧 Feature Extraction Provides

All these metrics are extracted from video analysis:
1. **movement_speed** - Normalized motion intensity (0-1)
2. **stability** - Inverse of movement variance (0-1)
3. **motion_smoothness** - Consistency of velocity (0-1)
4. **posture_deviation** - Spatial variance from center (0-1)
5. **micro_movements** - Small involuntary motions (0-1)
6. **range_of_motion** - Spatial coverage (0-1)
7. **acceleration_variance** - Speed pattern changes (0-1)
8. **frame_count** - Number of frames analyzed

## 📝 Data Flow

```
Daily Health Check Page
    ↓
1. Sit-to-Stand Test → extract_features() → 8 metrics
2. Stability Test → extract_features() → 8 metrics  
3. Movement Test → extract_features() → 8 metrics
    ↓
Combine & Calculate Averages
    ↓
save_health_check() → Supabase
    ↓
All 40+ columns populated ✅
```

## 🚀 Next Steps

1. **Run the updated SQL schema** in Supabase to add missing columns
2. **Restart your Streamlit app**
3. **Complete a Daily Health Check**
4. **Verify all columns are populated** in Supabase

All columns will now be filled with real data from your health assessments!
