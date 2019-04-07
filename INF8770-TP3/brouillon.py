
while(True):
    # Lire les frames de la vidéo.
    frame = video.read() 
    
    # Si première itération, garder en mémoire tmp les histogrammes de couleurs
    # et les arêtes pour la prochaine itération.
    if isFirstIteration:
        prevHistograms = histograms(frame)
        prevEdges, prevDilatedEdges = sobelConvolution(frame)

    # Sinon récupérer les histogrammes et arêtes pour comparaison.
    else:
        histograms = histograms(frame)
        edges, dilatedEdges = sobelConvolution(frame)

        # DÉCOMPOSITION EN PRISES DE VUE -> HISTOGRAMMES

        # Si la corrélation entre les histogrammes de la présente frame
        # et ceux de la frame précédente plus petite qu'un indice X,
        # alors on assume que c'est une coupure.
        if distance(histograms, prevHistograms) <= X:
            print("Histo -> Cut at frame : " + str(index))

        # Sinon, si c'est plus grand que X mais plus petit qu'un second
        # indice Y, c'est le début d'un fondu.
        elif distance(histograms, prevHistograms) <= Y:
            # Vérification si le statu de fondu est déjà activé.
            if not isFading:  
                isFading = True
                fadeStart = frame
        
        # Sinon, cela signalise qu'il n'y eu aucun effet de caméra ou bien que 
        # c'est la fin d'un fondu.
        else:
            if isFading:
                isFading = False
                fadeEnd = frame
                print("Histo -> Fade at frames : " + fadeStart + " to " + fadeEnd) 

        # DÉCOMPOSITION EN PRISES DE VUE -> COMPARAISON DES ARÊTES

        # Comparer les arêtes de la frame courante et précédente afin de 
        # récupérer le maximum(arêtes entrantes, arêtes sortantes). 
        maxp = maxEdges(edges, prevEdges, dilatedEdges, prevDilatedEdges)

        # Si un pic plus grand qu'un certain indice H est détecté, cela signifie
        # le début d'un effet de caméra.
        if abs(maxp - prevMaxp) >= H:
            isEffect = True
            effectStart = frame
            high = maxp # Nouveau pic
        
        # Sinon, si le statu d'effet est en cours, tant que le pic atteint ne varie
        # pas plus qu'un indice P, cela veut dire que l'effet est encore présent. Dans
        # le cas d'une fin d'effet, le nombre de frames qu'il a perdurer détermine si c'est
        # une coupure ou un fondu.
        else:
            if isEffect and abs(maxp - high) >= P:
                isEffect = False
                effectEnd = frame
                if (effectEnd - effectStart) == 1:
                    print("Convo -> Cut at frame : " + effectStart)
                else:    
                    print("Convo -> Fade at frames : " + effectStart + " to " + effectEnd)
        
        # Finalement, transferer les valeurs des histogrammes et des arêtes courantes
        # aux variables mémoires tmp pour les utiliser dans la prochaine itération. 
        prevMaxp = maxp 
        prevHistograms = histograms
        prevEdges = edges
        prevDilatedEdges = prevDilatedEdges