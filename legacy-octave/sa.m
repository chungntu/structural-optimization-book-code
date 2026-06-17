function plot_truss_template_demo()
  % =========================
  % DEMO DATA (b\u1ea1n thay b\u1eb1ng data c\u1ee7a b\u1ea1n)
  % =========================
  nodes = [ ...
    0 0;
    1 0;
    2 0;
    0 1;
    1 1;
    2 1
  ];

  % elements: [i j] (1-based index)
  elems = [ ...
    1 2; 2 3;
    4 5; 5 6;
    1 4; 2 5; 3 6;
    4 2; 5 3
  ];

  % supports: [node_id fixX fixY] (1 = fixed, 0 = free)
  supports = [ ...
    1 1 1;
    4 1 1
  ];

  % nodal loads: [node_id Fx Fy]
  loads = [ ...
    3 0 -1;
    6 0 -1
  ];

  % Optional results (n\u1ebfu b\u1ea1n c\u00f3)
  % U: size = (2*nnode, 1), [u1 v1 u2 v2 ...]'
  nnode = rows(nodes);
  U = zeros(2*nnode,1);
  U(2*3) = -0.03;   % demo v\u00f5ng
  U(2*6) = -0.02;

  % N: axial force per element (size = nelem x 1), (+) k\u00e9o, (-) n\u00e9n
  N = [ 1; 1; -1; -1; 0; 0; 0; 0.5; -0.5 ];

  % =========================
  % PLOT
  % =========================
  figure(1); clf;
  plot_truss(nodes, elems, supports, loads, ...
             "U", U, "deform_scale", 10, ...
             "N", N, "show_member_forces", true);
endfunction


function plot_truss(nodes, elems, supports, loads, varargin)
  % plot_truss(nodes, elems, supports, loads, "U", U, "deform_scale", s, "N", N, "show_member_forces", tf)
  %
  % nodes   : (n x 2) [x y]
  % elems   : (m x 2) [i j]  (1-based)
  % supports: (k x 3) [node_id fixX fixY]
  % loads   : (p x 3) [node_id Fx Fy]
  %
  % Options:
  %   "U" (2n x 1)            displacement vector
  %   "deform_scale" (scalar) scale factor for deformed shape
  %   "N" (m x 1)             axial forces per element
  %   "show_member_forces"    true/false

  % ---- defaults
  U = [];
  deform_scale = 1.0;
  N = [];
  show_member_forces = false;

  % ---- parse options
  i = 1;
  while i <= numel(varargin)
    key = varargin{i};
    if (i == numel(varargin)), error("Option %s missing value", key); endif
    val = varargin{i+1};
    switch lower(key)
      case "u"
        U = val;
      case "deform_scale"
        deform_scale = val;
      case "n"
        N = val;
      case "show_member_forces"
        show_member_forces = logical(val);
      otherwise
        error("Unknown option: %s", key);
    endswitch
    i += 2;
  endwhile

  % ---- cosmetics
  try, graphics_toolkit("qt"); catch, end_try_catch

  axis equal; hold on; box on;
  set(gca, "fontsize", 13, "linewidth", 1.2);
  xlabel("x"); ylabel("y");

  nnode = rows(nodes);
  nelem = rows(elems);

  % ---- draw undeformed truss
  lw = 2.0;
  for e = 1:nelem
    a = elems(e,1); b = elems(e,2);
    xa = nodes(a,1); ya = nodes(a,2);
    xb = nodes(b,1); yb = nodes(b,2);
    plot([xa xb],[ya yb], "-", "linewidth", lw);
  endfor

  % ---- draw nodes (white circles)
  plot(nodes(:,1), nodes(:,2), "o", "markersize", 7, "markerfacecolor", "w", "linewidth", 1.3);

  % ---- supports
  if !isempty(supports)
    draw_supports(nodes, supports);
  endif

  % ---- loads (arrows)
  if !isempty(loads)
    draw_loads(nodes, loads);
  endif

  % ---- deformed shape
  if !isempty(U)
    if rows(U) != 2*nnode, error("U must be (2*nnode x 1)"); endif
    def = nodes;
    def(:,1) += deform_scale * U(1:2:end);
    def(:,2) += deform_scale * U(2:2:end);

    % deformed elements (dashed)
    for e = 1:nelem
      a = elems(e,1); b = elems(e,2);
      plot([def(a,1) def(b,1)], [def(a,2) def(b,2)], "--", "linewidth", 1.6);
    endfor
    plot(def(:,1), def(:,2), "o", "markersize", 6, "markerfacecolor", "w", "linewidth", 1.2);
  endif

  % ---- member force coloring (optional)
  if show_member_forces && !isempty(N)
    if rows(N) != nelem, error("N must be (nelem x 1)"); endif
    overlay_member_forces(nodes, elems, N);
  endif

  title("Truss / Gi\u00e0n (Octave template)");
  legend_entries = {"Gi\u00e0n", "N\u00fat"};
  if !isempty(U), legend_entries{end+1} = "Bi\u1ebfn d\u1ea1ng"; endif
  legend(legend_entries, "location", "bestoutside");
  hold off;
endfunction


function draw_supports(nodes, supports)
  % Very simple icons:
  % - fixed in X & Y: square base (like pin/roller simplified)
  % - fixed only Y or X: smaller marker

  s = mean(range(nodes)); if s == 0, s = 1; endif
  a = 0.06*s;  % icon size

  for i = 1:rows(supports)
    nid = supports(i,1);
    fx  = supports(i,2);
    fy  = supports(i,3);
    x = nodes(nid,1); y = nodes(nid,2);

    if (fx==1 && fy==1)
      % "fixed" marker: small filled square + ground line
      plot(x, y, "s", "markersize", 9, "markerfacecolor", "k");
      plot([x-1.4*a x+1.4*a], [y-1.2*a y-1.2*a], "-", "linewidth", 2.0);
    else
      % partial constraint: triangle-ish marker
      plot([x-a x x+a x-a], [y-a y-1.3*a y-a y-a], "-", "linewidth", 2.0);
    endif
  endfor
endfunction


function draw_loads(nodes, loads)
  % Uses quiver; auto scaling for nicer arrows
  Fx = loads(:,2); Fy = loads(:,3);
  mag = max(sqrt(Fx.^2 + Fy.^2));
  if mag == 0, return; endif

  s = mean(range(nodes)); if s == 0, s = 1; endif
  scale = 0.18*s / mag;

  for i = 1:rows(loads)
    nid = loads(i,1);
    fx = loads(i,2); fy = loads(i,3);
    x = nodes(nid,1); y = nodes(nid,2);
    quiver(x, y, fx*scale, fy*scale, 0, "linewidth", 2.0, "maxheadsize", 0.8);
  endfor
endfunction


function overlay_member_forces(nodes, elems, N)
  % Overlay colored lines by axial force:
  % - tension (N>0): warm
  % - compression (N<0): cool
  % Note: Octave/MATLAB colors differ slightly, but this looks good.
  nelem = rows(elems);
  maxN = max(abs(N));
  if maxN == 0, maxN = 1; endif

  for e = 1:nelem
    a = elems(e,1); b = elems(e,2);
    xa = nodes(a,1); ya = nodes(a,2);
    xb = nodes(b,1); yb = nodes(b,2);

    t = N(e)/maxN;           % [-1..1]
    if t >= 0
      col = [0.85 0.2 0.2];  % tension
    else
      col = [0.2 0.35 0.85]; % compression
    endif
    alpha = 0.25 + 0.75*abs(t); % thickness factor
    plot([xa xb],[ya yb], "-", "linewidth", 3.2*alpha, "color", col);
  endfor

  % force legend text
  text(min(nodes(:,1)), max(nodes(:,2)), sprintf("N>0: k\u00e9o | N<0: n\u00e9n"), "fontsize", 12);
endfunction


function r = range(x)
  % helper: range along each column
  r = max(x) - min(x);
endfunction

