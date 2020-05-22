function sauverPourPython ( temps, grandeur )
% Ecrit grandeur et temps dans un fichier pour qu'ils puissent être réutilisés par le code python du projet SunRise. Le nom du fichier créé sera dérivé du nom de la variable passé en argument pour grandeur.

% Cette fonction est compatible avec GNU/Octave (en fait elle n'a même pas été testée sous MatLab, juste sous Octave).

% On commence par vérifier les arguments passés à la fonction
if nargin ~= 2
  error("Vous avez passé un nombre de paramètres incorrect à la fonction.");
endif
% sinon on vérifie que temps et grandeu sont bien compatible, c'est à dire qu'ils ont le même nombre d'éléments.
tailleTemps = size(temps);
tailleGrandeur = size(grandeur);
if tailleTemps ~= tailleGrandeur
  % Avant de lancer l'exception, on regarde si une transposition ne pourrait pas régler le problème. C'est une commodité pour simplifier l'usage de la fonction.
  transposeGrandeur = grandeur';
  tailleTranspose = size(transposeGrandeur);
  if tailleTranspose == tailleTemps
    % si cela fonctionne alors on travaille avec la transposée.
    grandeur = transposeGrandeur;
  else
    % Rien à faire, les deux tableaux ont vraiment des tailles différentes.
    error("Les tableaux temps et grandeur passés en argument ont des tailles différentes.");
  endif
endif
% sinon on écrit notre fichier.
matriceEcrite = [temps, grandeur];
% Le fait d'utiliser inputname n'est pas très robuste ni une bonne pratique, mais dans la mesure où ce code concerne du MatLab en premier lieu...
nomDuFichierCSV = strcat(inputname(2), '.csv');

% Enfin, on écrit la matrice créée sur le fichier dédié. La méthode d'écriture dépend de si le code est lancé sous MatLab ou Octave
if exist('OCTAVE_VERSION', 'builtin')
  % code lancé sous octave
  csvwrite(nomDuFichierCSV, matriceEcrite);
else
  % code lancé sous MatLab
  writematrix(matriceEcrite, nomDuFichierCSV);
endif
end  % function
