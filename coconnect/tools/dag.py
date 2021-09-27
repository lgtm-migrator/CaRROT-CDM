from graphviz import Digraph
import json

colorscheme = 'gnbu9'

def make_dag(data,render=False):
    _format = 'svg'
    if render == True:
        _format = 'pdf'

    dot = Digraph(strict=True,format=_format)
    dot.attr(rankdir='RL')#, size='20,8')
            
    # #dot.attr(rankdir='RL', size='8,16',compound='true')

    
    with dot.subgraph(name='cluster_0') as dest, dot.subgraph(name='cluster_1') as inp:
        
        #dest.attr(style='dotted',penwidth='4', label='CDM')
        #inp.attr(style='filled', fillcolor='lightgrey', penwidth='0', label='Input')
        
        dest.attr(style='filled', fillcolor='2', colorscheme='blues9', penwidth='0', label='Destination')
        inp.attr(style='filled', fillcolor='2', colorscheme='greens9', penwidth='0', label='Source')
        
        for destination_table_name,destination_tables in data.items():
            dest.node(destination_table_name,
                      shape='folder',style='filled',
                      fontcolor='white',colorscheme=colorscheme,
                      fillcolor='9')

            for ref_name,destination_table in destination_tables.items():
                for destination_field,source in destination_table.items():
                    source_field = source['source_field']
                    source_table = source['source_table']
                    
                    table_name = f"{destination_table_name}_{destination_field}"
                    dest.node(table_name,
                             label=destination_field,style='filled,rounded', colorscheme=colorscheme,
                             fillcolor='7',shape='box',fontcolor='white')

                    dest.edge(destination_table_name,table_name,arrowhead='inv')

                    source_field_name =  f"{source_table}_{source_field}"
                    inp.node(source_field_name,source_field,
                             colorscheme=colorscheme,
                             style='filled,rounded',fillcolor='5',shape='box')
                    
                    if 'operations' in source:
                        operations = source['operations']

                    if 'term_mapping' in source and source['term_mapping'] is not None:
                        term_mapping = source['term_mapping']
                        dot.edge(table_name,source_field_name,dir='back',color='red',penwidth='2')
                    else:                                                    
                        dot.edge(table_name,source_field_name,dir='back',penwidth='2')
                    
                    inp.node(source_table,shape='tab',fillcolor='4',colorscheme=colorscheme,style='filled')
                    inp.edge(source_field_name,source_table,dir='back',arrowhead='inv')


    #dot.subgraph(destinations)
    #dot.subgraph(sources)

    #destinations = dot.subgraph(name='cdm')
    #destinations = Digraph('cdm')
    #destinations.attr(style='dotted',rank='same',label='process #2')
    #dot.subgraph(destinations)
    #sources = Digraph('sources')
    #sources.attr(style='dotted',rank='same',label='process #1')

    
                
    if render:
        dot.render('person.gv', view=True)  
        return
    #    
    #return dot.pipe().decode('utf-8')

