"""
Add this code to your routes.py file to implement confidence scoring
"""

import json
import re
from collections import Counter

def calculate_confidence_score(extracted_data, original_text):
    """
    Calculate confidence score for extracted entities
    Returns: dict with entity: confidence pairs
    """
    confidence_scores = {}
    
    for field, value in extracted_data.items():
        if not value or value == "null" or value == "":
            confidence_scores[field] = 0.0
            continue
            
        # Check if value appears in original text (exact match)
        if value.lower() in original_text.lower():
            base_score = 0.9
        else:
            # Fuzzy match - check if parts of the value appear
            words = value.split()
            matches = sum(1 for word in words if len(word) > 3 and word.lower() in original_text.lower())
            base_score = 0.5 + (matches / len(words) * 0.3) if words else 0.3
        
        # Adjust based on field type
        if field in ['patientID', 'patientBirthDate']:
            # IDs and dates are usually more reliable
            base_score = min(base_score + 0.1, 1.0)
        
        # Length penalty for very short extractions
        if len(str(value)) < 3:
            base_score *= 0.7
            
        confidence_scores[field] = round(base_score, 2)
    
    return confidence_scores


def calculate_privacy_risk(extracted_data, confidence_scores):
    """
    Calculate privacy risk metrics
    Returns: dict with various risk metrics
    """
    # Count high-confidence personal identifiers
    high_risk_fields = ['patientName', 'patientFirstName', 'patientLastName', 
                        'patientBirthDate', 'patientID', 'patientStreet', 
                        'patientPostalCode', 'patientCity']
    
    detected_high_risk = 0
    total_high_risk = len(high_risk_fields)
    
    for field in high_risk_fields:
        if field in extracted_data and extracted_data[field]:
            if confidence_scores.get(field, 0) > 0.6:
                detected_high_risk += 1
    
    # Calculate risk score (0-100, higher = more risky if not anonymized)
    risk_before = (detected_high_risk / total_high_risk) * 100
    risk_after = max(0, risk_before - 85)  # After anonymization, risk should be minimal
    
    # K-anonymity estimation (simplified)
    unique_identifiers = detected_high_risk
    k_anonymity = max(1, 1000 // (2 ** unique_identifiers))  # Rough estimate
    
    # Re-identification risk
    reidentification_risk = "High" if detected_high_risk >= 5 else "Medium" if detected_high_risk >= 3 else "Low"
    
    return {
        'risk_before_anonymization': round(risk_before, 2),
        'risk_after_anonymization': round(risk_after, 2),
        'k_anonymity_estimate': k_anonymity,
        'reidentification_risk': reidentification_risk,
        'detected_identifiers': detected_high_risk,
        'total_possible_identifiers': total_high_risk,
        'privacy_preserved': round((1 - risk_after/100) * 100, 2)
    }


def get_entity_statistics(all_extractions):
    """
    Get statistics across multiple documents
    """
    entity_counts = Counter()
    avg_confidence = {}
    
    for extraction in all_extractions:
        for field, value in extraction.get('data', {}).items():
            if value and value != "null":
                entity_counts[field] += 1
        
        # Track confidence
        for field, conf in extraction.get('confidence', {}).items():
            if field not in avg_confidence:
                avg_confidence[field] = []
            avg_confidence[field].append(conf)
    
    # Calculate averages
    for field in avg_confidence:
        avg_confidence[field] = round(sum(avg_confidence[field]) / len(avg_confidence[field]), 2)
    
    return {
        'entity_counts': dict(entity_counts),
        'average_confidence': avg_confidence,
        'total_documents': len(all_extractions)
    }


# Example usage in your existing extraction code:
def process_document_with_confidence(report_text, model_response):
    """
    Wrapper function to add confidence and risk to existing extraction
    """
    # Your existing extraction logic here
    extracted_data = json.loads(model_response)  # Your existing parsing
    
    # Add confidence scores
    confidence_scores = calculate_confidence_score(extracted_data, report_text)
    
    # Calculate privacy risk
    privacy_risk = calculate_privacy_risk(extracted_data, confidence_scores)
    
    # Return enhanced result
    return {
        'data': extracted_data,
        'confidence': confidence_scores,
        'privacy_risk': privacy_risk,
        'overall_confidence': round(sum(confidence_scores.values()) / len(confidence_scores), 2) if confidence_scores else 0
    }