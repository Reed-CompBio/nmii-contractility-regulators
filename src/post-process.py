from graphspace_python.api.client import GraphSpace
from graphspace_python.graphs.classes.gsgraph import GSGraph
import random as rand
import sys

## Makes the networks, the final figures, and the final output files for the three methods.
## Last updated Aept 2023 by Anna Ritz
## Requires the graphspace Python module and an account on GraphSpace

def main(input_dir,output_dir,post_networks,post_focus_nets,username,password):
    post_focus_nets = False # post the flw/oya network?
    name_mapper = {'CG11811':'Oya'}

    # Import and arrange data
    # creates a discionary of FB identifiers and common names
    common_names_dict = read_common_names(input_dir+'/nodes-flybase.txt')

    network = {}
    for row in open(input_dir+'/interactome-flybase-collapsed-evidence.txt').readlines():
        split_row = row.strip().split()
        u = split_row[0]
        v = split_row[1]
        if u == v:
            continue

        if u not in network:
            network[u] = {}
        if v not in network:
            network[v] = {}
        network[u][v] = float(1)
        network[v][u] = float(1)
    print('network read in (no self loops).')

    pos = open(input_dir+'/positive-ids.txt').readlines()
    positives = set()
    for p in pos:
        p = p.strip()
        if p in common_names_dict:
            positives.add(common_names_dict[p])
    print('read in positives')

    steiner,steiner_edges = get_steiner(common_names_dict,network,positives)
    nmii,nmii_edges = get_nmii(common_names_dict,network,positives)
    ranked,ranked_edges,ranked_vals = get_ranked(common_names_dict,network,positives)

    s = steiner.difference(positives)
    n = nmii.difference(positives)
    r = ranked.difference(positives)
    write_final_files(s,n,r,output_dir)

    print('steiner %d nmii %d ranked %d' % (len(s),len(n),len(r)))
    print('steiner & nmii (%d):' % len(s.intersection(n)),s.intersection(n))
    print('steiner & ranked (%d):' % len(s.intersection(r)),s.intersection(r))
    print('nmii & ranked (%d):' % len(r.intersection(n)),r.intersection(n))
    print('All 3 (%d):' % len(s.intersection(n).intersection(r)),s.intersection(n).intersection(r))
    print('Total:',len(s.union(n).union(r)))

    graphspace = False

    ##NEW
    if post_networks:
        if graphspace == False:
            ## connect to GraphSpace
            graphspace = GraphSpace(username,password)
        color1 = rgb_to_hex(0.9,0.4,0.4)
        color2 = rgb_to_hex(0.4,0.8,0.2)
        color3 = rgb_to_hex(0.4,0.4,0.9)
        combined_color1 = rgb_to_hex(0.9,0.8,0.3) # 1 & 2
        combined_color2 = rgb_to_hex(0.9,0.4,0.9) # 1 & 3
        combined_color3 = rgb_to_hex(0.4,0.8,0.9) # 2 & 3
        combined_all_color = rgb_to_hex(1,1,1) # 1,2 & 3
        make_graph_single_method(graphspace,'Steiner %.4f' % (rand.random()),positives,steiner_edges,'Steiner',color1)
        make_graph_single_method(graphspace,'NMII %.4f' % (rand.random()),positives,nmii_edges,'NMII',color2)
        make_graph_single_method(graphspace,'Ranked %.4f' % (rand.random()),positives,ranked_edges,'Ranked',color3,vals=ranked_vals)

        make_graph_merged(graphspace,'Steiner & NMII %.4f' % (rand.random()),positives,steiner_edges,nmii_edges,'Steiner','NMII',color1,color2,combined_color1)

        make_graph_merged3(graphspace,'Steiner, NMII, & Ranked %.4f' % (rand.random()),positives,steiner_edges,nmii_edges,ranked_edges,'Steiner','NMII','Ranked',color1,color2,color3,combined_color1,combined_color2,combined_color3,combined_all_color)

    if post_focus_nets:
        if graphspace == False:
            ## connect to GraphSpace
            graphspace = GraphSpace(username,password)

        #make_focus_network(graphspace, 'Flw %.4f' % (rand.random()), 'flw',network,positives,name_mapper)
        preds = (steiner.union(nmii).union(ranked)).difference(positives)
        make_focus_network(graphspace, 'Oya %.4f' % (rand.random()), 'CG11811',network,positives,preds,name_mapper)

    return

def write_final_files(s,n,r,output_dir):
    out = open(output_dir+'/steiner-final.txt','w')
    out.write('\n'.join(x for x in sorted(s))+'\n')
    out.close()

    out = open(output_dir+'/nmii-final.txt','w')
    out.write('\n'.join(x for x in sorted(n))+'\n')
    out.close()

    out = open(output_dir+'/ranked-final.txt','w')
    out.write('\n'.join(x for x in sorted(r))+'\n')
    out.close()

    print('wrote *-final.txt files.')
    return

def get_steiner(d,network,positives):
    steiner_edges = set()
    steiner = set()
    with open(output_dir+'/collapsed_tree_edges.txt') as fin:
        for line in fin:
            if line[0] == '#':
                continue
            row = line.strip().split()
            if row[0] in d and row[1] in d:
                steiner_edges.add((d[row[0]],d[row[1]]))
                steiner.add(d[row[0]])
                steiner.add(d[row[1]])
    return steiner,steiner_edges

def get_nmii(d,network,positives):

    nmii_edges = set()
    nmii = set()
    with open(output_dir+'/collapsed_shortest_paths_from_sqh.txt') as fin:
        for line in fin:
            if line[0] == '#':
                continue
            row = line.strip().split()
            for i in range(1,len(row)):
                if row[i-1] in d and row[i] in d:
                    nmii_edges.add((d[row[i-1]],d[row[i]]))
                    nmii.add(d[row[i-1]])
                    nmii.add(d[row[i]])
    return nmii,nmii_edges

def get_ranked(d,network,positives):
    ranked = set(['sqh']) # have the network show sqh
    ranked_vals = {}
    thres = 0.7
    with open(output_dir+'/collapsed_shortestpaths_rank.txt') as fin:
        for line in fin:
            if line[0] == '#':
                continue
            row = line.strip().split()
            if row[0] in d and float(row[1]) > thres:
                ranked.add(d[row[0]])
                ranked_vals[d[row[0]]] = float(row[1])

    ranked_edges = set()
    seen = set()
    for u in ranked:
        for v in ranked:
            if u == v or (u,v) in seen:
                continue
            if v in network[u] or u in network[v]:
                ranked_edges.add((u,v))
                seen.add((u,v))
                seen.add((v,u))
    return ranked, ranked_edges,ranked_vals


## Input file: 'nodes-flybase.txt'
## Outputs a dictionary with flybase IDs as keys and common names as values
def read_common_names(filename):
    name_dict = {}
    with open (filename, 'r') as f:
        for line in f:
            k = line.strip().split()
            if k[2] is not k[0]:
                name_dict[k[0]] = k[2]
    #print('Name dictionary:' + str(name_dict))
    return name_dict

def rgb_to_hex(red,green,blue):
    maxHexValue = 255
    r = int(red*maxHexValue)
    g = int(green*maxHexValue)
    b = int(blue*maxHexValue)
    RR = format(r, '02x')
    GG = format(g, '02x')
    BB = format(b, '02x')
    return '#'+RR+GG+BB

# 1. make GS graph for all candidates
def make_graph_single_method(graphspace,title,positives,edges,method_label,method_color,vals=False):

    G = GSGraph()
    G.set_name(title)
    nodes = set([u for u,v in edges]).union(set([v for u,v in edges]))
    for n in nodes:
        height = 30
        width= 30
        if n in positives:
            color=rgb_to_hex(.9,.9,.9)
            popup='Positive'
        else:
            if vals:
                color = method_color
                popup = 'in %s set (rank=%.4f)' %(method_label,vals[n])
            else:
                color = method_color
                popup = 'in %s set' %(method_label)
        G.add_node(n,label=n,popup=popup)
        G.add_node_style(n,color=color,shape='ellipse',height=height,width=height)
    seen = set()
    for u,v in edges:
        if (u,v) not in seen:
            G.add_edge(u,v)
            if vals:
                G.add_edge_style(u,v,width=1) # used to be network[u][v]*3
            else:
                G.add_edge_style(u,v,width=3) # used to be network[u][v]*3
            seen.add((u,v))
            seen.add((v,u))

    post_gs_graph(graphspace,G)
    return

def make_graph_merged(graphspace,title,positives,edges1,edges2,method_label1,method_label2,color1,color2,combined_color):

    G = GSGraph()
    G.set_name(title)
    nodes1 = set([u for u,v in edges1]).union(set([v for u,v in edges1]))
    nodes2 = set([u for u,v in edges2]).union(set([v for u,v in edges2]))
    all_nodes = nodes1.union(nodes2)
    for n in all_nodes:
        height = 30
        width= 30
        label=n
        if n in positives:
            color=rgb_to_hex(.9,.9,.9)
            popup='Positive: '+n
        elif n in nodes1 and n in nodes2:
            color = combined_color
            popup = 'in both %s and %s' %(method_label1,method_label2)
            height=50
            width=50
        elif n in nodes1:
            color = color1
            popup = 'in %s' % (method_label1)
        elif n in nodes2:
            color =color2
            popup = 'in %s' % (method_label2)
        else:
            sys.exit('ERROR: NODE ISN\'T A POSITIVE OR IN A METHOD')

        G.add_node(n,label=label,popup=popup)
        G.add_node_style(n,color=color,shape='ellipse',height=height,width=height)

    seen = set()
    all_edges = edges1.union(edges2)
    for u,v in all_edges:
        if (u,v) not in seen:
            G.add_edge(u,v)
            G.add_edge_style(u,v,width=2)
            seen.add((u,v))
            seen.add((v,u))

    post_gs_graph(graphspace,G)
    return

def make_graph_merged3(graphspace,title,positives,edges1,edges2,edges3,method_label1,method_label2,method_label3,color1,color2,color3,combined_color1,combined_color2,combined_color3,combined_color_all):

    G = GSGraph()
    G.set_name(title)
    nodes1 = set([u for u,v in edges1]).union(set([v for u,v in edges1]))
    nodes2 = set([u for u,v in edges2]).union(set([v for u,v in edges2]))
    nodes3 = set([u for u,v in edges3]).union(set([v for u,v in edges3]))
    all_nodes = nodes1.union(nodes2).union(nodes3)
    node_counter = {'1':0,'2':0,'3':0,'12':0,'13':0,'23':0,'123':0}
    for n in all_nodes:
        height = 30
        width= 30
        label=n
        if n in positives:
            color=rgb_to_hex(.9,.9,.9)
            popup='Positive: '+n
        elif n in nodes1 and n in nodes2 and n in nodes3:
            color = combined_color_all
            popup = 'in all %s, %s, and %s' %(method_label1,method_label2,method_label3)
            height=70
            width=70
            node_counter['123']+=1
        elif n in nodes1 and n in nodes2:
            color = combined_color1
            popup = 'in both %s and %s' %(method_label1,method_label2)
            height=50
            width=50
            node_counter['12']+=1
        elif n in nodes1 and n in nodes3:
            color = combined_color2
            popup = 'in both %s and %s' %(method_label1,method_label3)
            height=50
            width=50
            node_counter['13']+=1
        elif n in nodes2 and n in nodes3:
            color = combined_color3
            popup = 'in both %s and %s' %(method_label2,method_label3)
            height=50
            width=50
            node_counter['23']+=1
        elif n in nodes1:
            color = color1
            popup = 'in %s' % (method_label1)
            node_counter['1']+=1
        elif n in nodes2:
            color =color2
            popup = 'in %s' % (method_label2)
            node_counter['2']+=1
        elif n in nodes3:
            color =color3
            popup = 'in %s' % (method_label3)
            node_counter['3']+=1
        else:
            sys.exit('ERROR: NODE ISN\'T A POSITIVE OR IN A METHOD')

        G.add_node(n,label=label,popup=popup)
        G.add_node_style(n,color=color,shape='ellipse',height=height,width=height)
    #print('NODE COUNTS',node_counter)
    seen = set()
    all_edges = edges1.union(edges2).union(edges3)
    for u,v in all_edges:
        if (u,v) not in seen:
            G.add_edge(u,v)
            G.add_edge_style(u,v,width=1)
            seen.add((u,v))
            seen.add((v,u))

    post_gs_graph(graphspace,G)
    return


# 2. Make focus networks
def make_focus_network(graphspace, title, node,network,positives,preds,name_mapper):
    G = GSGraph()
    G.set_name(title)
    nodes = set(network[node].keys())
    nodes.add(node)
    print(nodes)
    print(len(nodes))
    print(node)
    for n in nodes:
        height = 30
        width= 30
        popup = n
        shape='rectangle'
        if n == node:
            color = rgb_to_hex(.9,.6,.9)
            height=50
            width=50
            shape='ellipse'
            popup = '%s (%s)' % (n,name_mapper.get(n,n))
        elif n in positives:
            color=rgb_to_hex(.8,.8,.8)
            popup='Positive'
            width=75
        elif n in preds:
            color=rgb_to_hex(.5,.9,.5)
            popup='Predicted by Some Method'
            width=75
        else:
            color = rgb_to_hex(1,1,1)
            width=57
        G.add_node(n,label=name_mapper.get(n,n),popup=popup)
        G.add_node_style(n,color=color,shape=shape,height=height,width=width)
    seen = set()
    for u in nodes:
        for v in nodes:
            if u != v and v in network[u] and (u,v) not in seen:
                G.add_edge(u,v)
                G.add_edge_style(u,v,width=3)
                seen.add((u,v))
                seen.add((v,u))

    post_gs_graph(graphspace,G)
    return


def post_gs_graph(graphspace,G):
    try:
        graph = graphspace.update_graph(G)
        print('updated graph')
    except:
        graph = graphspace.post_graph(G)
    print('posted graph')

if __name__ == '__main__':
    if len(sys.argv) != 7:
        sys.exit('USAGE: post-process.py <INPUT_DIR> <OUTPUT_DIR> <POST_NETS> <POST_FOCUS_NETS> <USERNAME> <PASSWORD>\n\t<INPUT_DIR> Directory of input files\n\t<OUTPUT_DIR> Directory of output files (outputs of run.py)\n\t<POST_NETS> (True/False) posts the method networks\n\t<POST_FOCUS_NETS> (True/False) posts the Oya network\n\t<USERNAME> GraphSpace Username (email address)\n\t<PASSWORD> GraphSpace Password')
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    post_networks = sys.argv[3] == 'True' or sys.argv[3] == 'true'
    post_focus_nets = sys.argv[4] == 'True' or sys.argv[4] == 'true'
    username = sys.argv[5]
    password = sys.argv[6]
    print('INPUTS:',input_dir,output_dir,post_networks,post_focus_nets,username,password)
    main(input_dir,output_dir,post_networks,post_focus_nets,username,password)
