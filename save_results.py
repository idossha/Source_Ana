import os
import pandas as pd
import numpy as np
from collections import Counter
from utils import collect_wave_level_data

def save_statistical_results(analysis_results, output_dir="."):
    """Save statistical results for individual protocols to CSV files"""
    print("\n=== Saving Statistical Results for Individual Protocols ===")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save involvement statistics
    involvement_stats_data = []
    for protocol, results in analysis_results.items():
        for stage, stats_data in results['involvement_stats'].items():
            involvement_stats_data.append({
                'Protocol': protocol,
                'Stage': stage,
                'Mean_Involvement': stats_data['mean'],
                'Median_Involvement': stats_data['median'],
                'Std_Involvement': stats_data['std'],
                'Count': stats_data['count']
            })
    
    involvement_stats_df = pd.DataFrame(involvement_stats_data)
    involvement_stats_file = os.path.join(output_dir, "involvement_statistics.csv")
    involvement_stats_df.to_csv(involvement_stats_file, index=False)
    print(f"Saved involvement statistics to {involvement_stats_file}")
    
    # Save origin statistics for each protocol
    origin_files = []
    for protocol, results in analysis_results.items():
        origin_data = []
        for stage, stage_info in results['origin_data'].items():
            region_counts = stage_info['region_counts']
            total_waves = stage_info['total_waves']
            for region, count in region_counts.items():
                percentage = (count / total_waves * 100) if total_waves > 0 else 0
                origin_data.append({
                    'Protocol': protocol,
                    'Stage': stage,
                    'Region': region,
                    'Count': count,
                    'Total_Waves': total_waves,
                    'Percentage': percentage
                })
        if origin_data:
            origin_df = pd.DataFrame(origin_data)
            origin_file = os.path.join(output_dir, f"{protocol}_origin_statistics.csv")
            origin_df.to_csv(origin_file, index=False)
            origin_files.append(origin_file)
            print(f"Saved origin statistics for {protocol} to {origin_file}")
    
    # Save statistical test results
    all_test_results = []
    for protocol, results in analysis_results.items():
        # Add protocol information to each test result
        for result in results.get('involvement_test_results', []):
            result_copy = result.copy()
            result_copy['Protocol'] = protocol
            all_test_results.append(result_copy)
        
        for result in results.get('origin_test_results', []):
            result_copy = result.copy()
            result_copy['Protocol'] = protocol
            all_test_results.append(result_copy)
    
    stats_file = None
    if all_test_results:
        stats_df = pd.DataFrame(all_test_results)
        stats_file = os.path.join(output_dir, "statistical_test_results.csv")
        stats_df.to_csv(stats_file, index=False)
        print(f"Saved statistical test results to {stats_file}")
    
    return {
        'involvement_stats': involvement_stats_file,
        'origin_stats': origin_files,
        'test_results': stats_file
    }

def save_treatment_comparison_results(treatment_comparison_results, output_dir="."):
    """Save treatment comparison results to CSV files"""
    print("\n=== Saving Treatment Comparison Results ===")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save treatment involvement statistics
    treatment_involvement_stats = treatment_comparison_results['treatment_involvement_stats']
    involvement_data = []
    
    for group, stats_by_stage in treatment_involvement_stats.items():
        for stage, stats in stats_by_stage.items():
            involvement_data.append({
                'Treatment_Group': group,
                'Stage': stage,
                'Mean_Involvement': stats['mean'],
                'Median_Involvement': stats['median'],
                'Std_Involvement': stats['std'],
                'Count': stats['count']
            })
    
    involvement_df = pd.DataFrame(involvement_data)
    involvement_file = os.path.join(output_dir, "treatment_involvement_statistics.csv")
    involvement_df.to_csv(involvement_file, index=False)
    print(f"Saved treatment involvement statistics to {involvement_file}")
    
    # Save treatment origin statistics
    treatment_origin_data = treatment_comparison_results['treatment_origin_data']
    origin_data = []
    
    for group, origin_by_stage in treatment_origin_data.items():
        for stage, stage_info in origin_by_stage.items():
            region_counts = stage_info['region_counts']
            total_waves = stage_info['total_waves']
            for region, count in region_counts.items():
                percentage = (count / total_waves * 100) if total_waves > 0 else 0
                origin_data.append({
                    'Treatment_Group': group,
                    'Stage': stage,
                    'Region': region,
                    'Count': count,
                    'Total_Waves': total_waves,
                    'Percentage': percentage
                })
    
    if origin_data:
        origin_df = pd.DataFrame(origin_data)
        origin_file = os.path.join(output_dir, "treatment_origin_statistics.csv")
        origin_df.to_csv(origin_file, index=False)
        print(f"Saved treatment origin statistics to {origin_file}")
    else:
        origin_file = None
    
    # Save treatment comparison test results
    comparison_tests = treatment_comparison_results.get('treatment_comparison_tests', [])
    tests_file = None
    
    if comparison_tests:
        tests_df = pd.DataFrame(comparison_tests)
        tests_file = os.path.join(output_dir, "treatment_comparison_test_results.csv")
        tests_df.to_csv(tests_file, index=False)
        print(f"Saved treatment comparison test results to {tests_file}")
    
    return {
        'treatment_involvement_stats': involvement_file,
        'treatment_origin_stats': origin_file,
        'treatment_comparison_tests': tests_file
    }

def save_overall_treatment_comparison_results(overall_comparison_results, output_dir="."):
    """Save overall treatment comparison results to CSV files"""
    print("\n=== Saving Overall Treatment Comparison Results ===")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save overall involvement statistics
    involvement_stats = overall_comparison_results['overall_involvement_stats']
    involvement_data = []
    
    for group, stats_by_stage in involvement_stats.items():
        for stage, stats in stats_by_stage.items():
            involvement_data.append({
                'Treatment_Group': group,
                'Stage': stage,
                'Mean_Involvement': stats['mean'],
                'Median_Involvement': stats['median'],
                'Std_Involvement': stats['std'],
                'Count': stats['count']
            })
    
    involvement_df = pd.DataFrame(involvement_data)
    involvement_file = os.path.join(output_dir, "overall_involvement_statistics.csv")
    involvement_df.to_csv(involvement_file, index=False)
    print(f"Saved overall involvement statistics to {involvement_file}")
    
    # Save overall origin statistics
    origin_data = overall_comparison_results['overall_origin_data']
    origin_list = []
    
    for group, origin_by_stage in origin_data.items():
        for stage, stage_info in origin_by_stage.items():
            region_counts = stage_info['region_counts']
            total_waves = stage_info['total_waves']
            for region, count in region_counts.items():
                percentage = (count / total_waves * 100) if total_waves > 0 else 0
                origin_list.append({
                    'Treatment_Group': group,
                    'Stage': stage,
                    'Region': region,
                    'Count': count,
                    'Total_Waves': total_waves,
                    'Percentage': percentage
                })
    
    if origin_list:
        origin_df = pd.DataFrame(origin_list)
        origin_file = os.path.join(output_dir, "overall_origin_statistics.csv")
        origin_df.to_csv(origin_file, index=False)
        print(f"Saved overall origin statistics to {origin_file}")
    else:
        origin_file = None
    
    # Save overall comparison test results
    comparison_tests = overall_comparison_results.get('overall_comparison_tests', [])
    tests_file = None
    
    if comparison_tests:
        tests_df = pd.DataFrame(comparison_tests)
        tests_file = os.path.join(output_dir, "overall_comparison_test_results.csv")
        tests_df.to_csv(tests_file, index=False)
        print(f"Saved overall comparison test results to {tests_file}")
    
    return {
        'overall_involvement_stats': involvement_file,
        'overall_origin_stats': origin_file,
        'overall_comparison_tests': tests_file
    }

def save_proto_specific_comparison_results(proto_specific_results, output_dir="."):
    """Save proto-specific comparison results to CSV files"""
    print("\n=== Saving Proto-Specific Comparison Results ===")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save proto-specific involvement statistics
    involvement_data = []
    
    for protocol, results in proto_specific_results['proto_specific_results'].items():
        for group, stats_by_stage in results['involvement_stats'].items():
            for stage, stats in stats_by_stage.items():
                involvement_data.append({
                    'Protocol': protocol,
                    'Treatment_Group': group,
                    'Stage': stage,
                    'Mean_Involvement': stats['mean'],
                    'Median_Involvement': stats['median'],
                    'Std_Involvement': stats['std'],
                    'Count': stats['count']
                })
    
    involvement_df = pd.DataFrame(involvement_data)
    involvement_file = os.path.join(output_dir, "proto_specific_involvement_statistics.csv")
    involvement_df.to_csv(involvement_file, index=False)
    print(f"Saved proto-specific involvement statistics to {involvement_file}")
    
    # Save proto-specific origin statistics
    origin_list = []
    
    for protocol, results in proto_specific_results['proto_specific_results'].items():
        for group, origin_by_stage in results['origin_data'].items():
            for stage, stage_info in origin_by_stage.items():
                region_counts = stage_info['region_counts']
                total_waves = stage_info['total_waves']
                for region, count in region_counts.items():
                    percentage = (count / total_waves * 100) if total_waves > 0 else 0
                    origin_list.append({
                        'Protocol': protocol,
                        'Treatment_Group': group,
                        'Stage': stage,
                        'Region': region,
                        'Count': count,
                        'Total_Waves': total_waves,
                        'Percentage': percentage
                    })
    
    if origin_list:
        origin_df = pd.DataFrame(origin_list)
        origin_file = os.path.join(output_dir, "proto_specific_origin_statistics.csv")
        origin_df.to_csv(origin_file, index=False)
        print(f"Saved proto-specific origin statistics to {origin_file}")
    else:
        origin_file = None
    
    # Save proto-specific comparison test results
    all_tests = []
    
    for protocol, results in proto_specific_results['proto_specific_results'].items():
        for test in results.get('comparison_tests', []):
            test_copy = test.copy()
            if 'Protocol' not in test_copy:
                test_copy['Protocol'] = protocol
            all_tests.append(test_copy)
    
    tests_file = None
    if all_tests:
        tests_df = pd.DataFrame(all_tests)
        tests_file = os.path.join(output_dir, "proto_specific_comparison_test_results.csv")
        tests_df.to_csv(tests_file, index=False)
        print(f"Saved proto-specific comparison test results to {tests_file}")
    
    return {
        'proto_specific_involvement_stats': involvement_file,
        'proto_specific_origin_stats': origin_file,
        'proto_specific_comparison_tests': tests_file
    }

def save_within_group_stage_comparison_results(within_group_results, output_dir="."):
    """Save within-group stage comparison results to CSV files"""
    print("\n=== Saving Within-Group Stage Comparison Results ===")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save within-group involvement statistics
    involvement_data = []
    
    for group, results in within_group_results['within_group_results'].items():
        for stage, stats in results['involvement_stats'].items():
            involvement_data.append({
                'Treatment_Group': group,
                'Stage': stage,
                'Mean_Involvement': stats['mean'],
                'Median_Involvement': stats['median'],
                'Std_Involvement': stats['std'],
                'Count': stats['count']
            })
    
    involvement_df = pd.DataFrame(involvement_data)
    involvement_file = os.path.join(output_dir, "within_group_involvement_statistics.csv")
    involvement_df.to_csv(involvement_file, index=False)
    print(f"Saved within-group involvement statistics to {involvement_file}")
    
    # Save within-group origin statistics
    origin_list = []
    
    for group, results in within_group_results['within_group_results'].items():
        for stage, stage_info in results['origin_data'].items():
            region_counts = stage_info['region_counts']
            total_waves = stage_info['total_waves']
            for region, count in region_counts.items():
                percentage = (count / total_waves * 100) if total_waves > 0 else 0
                origin_list.append({
                    'Treatment_Group': group,
                    'Stage': stage,
                    'Region': region,
                    'Count': count,
                    'Total_Waves': total_waves,
                    'Percentage': percentage
                })
    
    if origin_list:
        origin_df = pd.DataFrame(origin_list)
        origin_file = os.path.join(output_dir, "within_group_origin_statistics.csv")
        origin_df.to_csv(origin_file, index=False)
        print(f"Saved within-group origin statistics to {origin_file}")
    else:
        origin_file = None
    
    # Save within-group test results
    all_tests = []
    
    for group, results in within_group_results['within_group_results'].items():
        for test in results.get('involvement_test_results', []) + results.get('origin_test_results', []):
            test_copy = test.copy()
            test_copy['Treatment_Group'] = group
            all_tests.append(test_copy)
    
    tests_file = None
    if all_tests:
        tests_df = pd.DataFrame(all_tests)
        tests_file = os.path.join(output_dir, "within_group_test_results.csv")
        tests_df.to_csv(tests_file, index=False)
        print(f"Saved within-group test results to {tests_file}")
    
    return {
        'within_group_involvement_stats': involvement_file,
        'within_group_origin_stats': origin_file,
        'within_group_test_results': tests_file
    }

# The save_meta_results function has been removed as it doesn't separate treatment groups
