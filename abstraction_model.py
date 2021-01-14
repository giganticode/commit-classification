# Design patterns list is based on wikipedia https://en.wikipedia.org/wiki/Software_design_pattern
import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX, VERB_E_SUFFIX, NEAR_ENOUGH\
 , programming_languges, software_goals
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier

"""
interface, encapsulation, composition, coupling, single responsibility, Liskov, virtual method, design, design patterns
, inheritance, Structured programming, ADT (abstract data type),  polymorphism, delegation, template, generic, object oriented
, Refinement, Reification
, liskov substitution principle
, solid, dry principle, composition, reuse
"""
core_abstraction_terms = [
'abstraction',
'abtract'  + REGULAR_SUFFIX,
'adapter(?:s)?',
'adt',# Abstract Data Type
'bridge(?:s)?',
'chain of responsibility',
'coherenc(?:e|y)',
'cohesion',
'composite',
'compos' + VERB_E_SUFFIX,
'composition',
'coupl(ed|ing)', # Note couples is missing since it common meaning is different
'controler(?:s)?',
'de(?: |-)?compos'  + VERB_E_SUFFIX,
'de(?: |-)?composition',
'de(?: |-)?coupl'  + VERB_E_SUFFIX,
'decorator(?:s)?',
'delegat' + VERB_E_SUFFIX,
'delegation',
'dependabilit(?:y|ies)',
'remov' + VERB_E_SUFFIX + NEAR_ENOUGH + 'dependenc(?:y|ies)'
#'dependenc(?:y|ies)',
'dependency injection',
'dependency inversion',
'design',
'design(?: |-)pattern(?:s)?',
'dry principle', # Don't Repeat Yourself
'duplication',
'duplicat' + VERB_E_SUFFIX,
'encapsulat' + VERB_E_SUFFIX,
'encapsulation',
'facade(?:s)?',
'factory',
'flyweight(?:s)?',
'generic(?:s)?',
'inheritance',
'interface',
'interface segregation',
'iterator(?:s)?',
'lazy initialization',
'liskov', # Liskov substitution principle
#'marker(?:s)?',
'mediator',
'memento',
'multiton',
'object(?:s)?(?: |-)pool(?:s)?',
'observer(?:s)?',
'object(?: |-)oriented',
'open(?: |-)closed principle',
'polymorphism',
'prototype(?:s)?',
'prox(?:y|ies)',
'publisher(?:s)?',
'pub(?: |-|/)sub',
're(?: |-)?us' + VERB_E_SUFFIX,
're(?: |-)?useability',
'refinement',
'reification',
'resource acquisition is initialization',
'raii', # Resource acquisition is initialization (RAII)
'single responsibility',
'singleton',
'solid', # SOLID principles
'structured programming',
'subscriber(?:s)?',
'servant',
'specification(?:s)?', # consider
#'state(?:s)?', # consider
'strateg(?:y|ies)',
'sub(?:-| )?class(?:es)?',
'super(?:-| )?class(?:es)?',
'template(?:s)?',
'testabil(?:e|ity)',
'twins(?:s)?',
#'translator(?:s)?', # more common for languages
'virtual method',
'visitor(?:s)?',
'(walker) state',
'wrapper(?:s)?',

]






excluded_abstraction_terms = ['reduc(es|e|ed|ing) abstraction'
, 'updat' + VERB_E_SUFFIX + NEAR_ENOUGH + 'dependenc(?:y|ies)'
, 'upgrad' + VERB_E_SUFFIX + NEAR_ENOUGH + 'dependenc(?:y|ies)'
, '(useless|bad) abstraction']

# Corrective
def build_core_abstraction_regex():

    return build_sepereted_term(core_abstraction_terms)



def build_excluded_abstraction_regex():

    return build_sepereted_term(excluded_abstraction_terms)


def build_not_abstraction_regex():

    return build_non_positive_linguistic(build_core_abstraction_regex())


def is_abstraction(commit_text):

    return (len(re.findall(build_core_abstraction_regex(), commit_text.lower()))
            - len(re.findall(build_excluded_abstraction_regex(), commit_text.lower()))
            - len(re.findall(build_not_abstraction_regex(), commit_text.lower()))
            )> 0



def print_abstraction_to_bq():
    concept = 'abstraction'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_abstraction(message)".format(schema=SCHEMA_NAME))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_abstraction(message)".format(schema=SCHEMA_NAME))

    print(" - ")
    print("# " + concept +  ": not positive")
    print("{schema}.bq_not_abstraction(message)".format(schema=SCHEMA_NAME))
    print("# end - " + concept)


def print_abstractionfunctions_for_bq(commit: str = 'XXX'):

    concepts = {'core_abstraction' : build_core_abstraction_regex
                , 'excluded_abstraction': build_excluded_abstraction_regex
                , 'not_abstraction': build_not_abstraction_regex
                #, 'abstraction': print_abstraction_to_bq
                }

    for i in concepts.keys():
        print()
        print_func = lambda : print_logic_to_bq(regex_func=concepts[i]
                                                , concept=i)
        generate_bq_function('{schema}.bq_{concept}'.format(schema=SCHEMA_NAME
                                                            , concept=i)
                             , print_func
                             , commit=commit)
        print()


    generate_bq_function('{schema}.bq_{concept}'.format(schema=SCHEMA_NAME
                                                        , concept='abstraction')
                         , print_abstraction_to_bq
                         , commit=commit)


def evaluate_abstraction_classifier():
    text_name = 'message'
    classification_function = is_abstraction
    classification_column = 'abstraction_pred'

    concept_column = 'Is_abstraction'

    df = pd.read_csv(join(DATA_PATH, 'abstraction_commits.csv'))


    df = classifiy_commits_df(df
                              , classification_function=classification_function
                              , classification_column=classification_column
                              , text_name=text_name
                              )
    cm = evaluate_performance(df
                              , classification_column
                              , concept_column
                              , text_name=text_name)
    print("Abstraction labels CM")
    print(cm)

if __name__ == '__main__':
    print_abstractionfunctions_for_bq(commit='0b713a426271a9ce9c8463ac224496ff8c99e138')
    #evaluate_cc_fix_classifier()

    text = """
"	* dvp-opc.c (parse_vif_unpackloc,insert_vif_unpackloc): Delete.
	(vif_operands): Update.
	(vif_get_unpackloc): Delete.
	(state_vif_unpackloc{,_star_p}): Delete.
	(dvp_opcode_init_parse): Update.
"    """.lower()

    print("is_abstraction", is_abstraction(text))
    valid_num = len(re.findall(build_core_abstraction_regex(), text))
    print(re.findall(build_core_abstraction_regex(), text))

