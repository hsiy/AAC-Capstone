"""
This file contains helper functions for text processing.
"""
import string


# Helper functions for text processing
# Since textblob or NLTK have required static files, and heroku is
# a pain in the butt when dealing with those, I've decided
# to take a naiive and simplistic approach to text processing,
# only using the precise heuristics I need, and nothing further

# Returns a dictionary containing blooms suggestions and
# whether or not the given input SLO is complex

def create_suggestions_dict(in_string):
    """
    Creates suggestion dictionary

    Args:
        in_string (str): string to create suggestions for

    Returns:
        dict : dictionary containing Blooms and Complexity suggestion
    
    """
    sug_dict = {
        'blooms' : blooms_suggestion(in_string),
        'complex' : is_complex(in_string)
    }

    return(sug_dict)

# Returns a string corresponding to a Bloom's taxonomy
def blooms_suggestion(in_string):
    """
    Creates suggestion of Bloom's taxonomy level

    Args:
        in_string (str) : input string to generate suggestions from

    Returns:
        str : suggested level
    """
    create_words = ['design', 'assemble', 'construct', 'conjecture', 'develop',
                    'formulate', 'author', 'investigate', 'create', 'adapt', 'plan',
                    'produce', 'build', 'solve', 'compose', 'think', 'theorize', 'modify',
                    'improve']
    evaluate_words = ['appraise', 'argue', 'defend', 'judge', 'select', 'support',
                      'value', 'critique', 'weigh', 'evaluate', 'assess', 'compare', 'conclude',
                      'debate', 'decide', 'measure', 'opinion', 'prove', 'support', 'test', 
                      'validate', 'interpret']
    analyze_words = ['differentiate', 'organize', 'relate', 'compare', 'contrast',
                     'distinguish', 'examine', 'experiment', 'question', 'test',
                     'analyze', 'arrange', 'breakdown', 'categorize', 'differences',
                     'dissect', 'inspect', 'research', 'highlight', 'find', 'question']
    apply_words = ['execute', 'implement', 'solve', 'use', 
                   'interpret', 'operate', 'schedule', 'sketch', 'apply',
                   'act', 'administer', 'build', 'choose', 'connect', 'construct', 'develop',
                   'teach', 'plan', 'employ', 'demonstrate', 'show']
    understand_words = ['describe', 'explain', 'identify', 'locate', 'recognize', 'report', 
                        'select', 'translate', 'understand', 'ask', 'cite', 'classify', 
                        'compare', 'contrast', 'discuss', 'rephrase', 'infer', 'summarize', 
                        'purpose', 'show', 'demonstrate', 'express', 'examples']
    remember_words = ['define', 'duplicate', 'list', 'memorize', 'repeat', 'state',
                      'remember', 'copy', 'recognize', 'tell', 'reproduce', 'retell',
                      'recite', 'read', 'knowledge']

    score_dict = {
        'Evaluation' : 0,
        'Synthesis' : 0,
        'Analysis' : 0,
        'Application' : 0,
        'Comprehension' : 0,
        'Knowledge' : 0,
    }

    for word in in_string.lower().split(' '):
        tword = word.translate(str.maketrans("","", string.punctuation))
        if tword in create_words:
            score_dict['Synthesis'] += 1
        elif tword in evaluate_words:
            score_dict['Evaluation'] += 1
        elif tword in analyze_words:
            score_dict['Analysis'] += 1
        elif tword in apply_words:
            score_dict['Application'] += 1
        elif tword in understand_words:
            score_dict['Comprehension'] += 1
        elif tword in remember_words:
            score_dict['Knowledge'] += 1

    suggestion = max(score_dict, key=score_dict.get)
    if score_dict[suggestion] == 0:
        suggestion = 'none'

    return(suggestion)


def is_complex(in_string):
    """
    Returns a boolean stating whether the given phrase is complex
    complexity is measured by having more than 3 words belonging to
    the following set: and, or, but

    Args:
        in_string (str): string to evaluate complexity of
    Returns:
        bool : whether the string should be considered complex
    """
    conjunctions = ['and', 'or', 'but']
    max_conjs = 3
    num_conjs = 0

    for word in in_string.split(" "):
        tword = word.translate(str.maketrans("","", string.punctuation))
        if tword in conjunctions:
            num_conjs += 1
    
    if num_conjs > max_conjs:
        return True
    return False