from ..models import Test

def statistical_probability(bacteria, antibiotic):

    total = Test.objects.filter(
        bacteria_name=bacteria,
        antibiotic_name=antibiotic
    ).count()

    if total == 0:
        return 0.5

    resistant = Test.objects.filter(
        bacteria_name=bacteria,
        antibiotic_name=antibiotic,
        result="R"
    ).count()

    return resistant / total