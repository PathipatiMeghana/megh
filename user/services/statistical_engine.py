from ..models import TestRecord

def statistical_probability(bacteria, antibiotic):
    total = TestRecord.objects.filter(
        bacteria=bacteria,
        antibiotic=antibiotic
    ).count()

    if total == 0:
        return 0.5  # Neutral default

    # A record represents a resistant case if:
    # 1. Prediction was "Resistant" and it WAS correct
    # 2. Prediction was "Susceptible" and it was NOT correct
    resistant_count = TestRecord.objects.filter(
        bacteria=bacteria,
        antibiotic=antibiotic,
        prediction="Resistant",
        is_correct=True
    ).count() + TestRecord.objects.filter(
        bacteria=bacteria,
        antibiotic=antibiotic,
        prediction="Susceptible",
        is_correct=False
    ).count()

    return resistant_count / total