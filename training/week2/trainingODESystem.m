function trainingODESystem
% Plots the time series of a very simple 6-species network
% The network includes the following reactions:
%   A + B -> C + D          (with rate constant k1)
%   C -> E + F              (with rate constant k2)
%   D -> B                  (with rate constant k3);
%
% Based on example code by Brian Ingalls:
% http://www.math.uwaterloo.ca/~bingalls/MMSB/Code/matlab/network_example.m

% Rate constant parameters
k1 = 3; % mM/sec
k2 = 1; % 1/sec
k3 = 4; % 1/sec
parameters = [k1 k2 k3];

% Initial species concentrations
S0 = [1,1,0.5,0,0,0];

% Set ODE simulation parameters
ODE=@trainingODEdt;
options=odeset('Refine', 6);
Tend=10;

% Run simulation
[t,S]=ode45(ODE, [0,Tend], S0, options, parameters);

% Plot time series
figure;
plot(t, S(:,1), 'k', t, S(:,2), 'k--', t, S(:,3),'b', ...
     t, S(:,4), 'b--', t, S(:,5), 'g', t, S(:,6), 'g--', 'Linewidth', 2)
legend('A', 'B', 'C', 'D', 'E', 'F')
xlabel('Time (sec)')
ylabel('Concentration (mM)')
 
end

function dS = trainingODEdt( ~, s, p )
% Simple ODE system for training purposes

    % Production and degradation terms
    k1 = p(1);
    k2 = p(2);
    k3 = p(3);
    
    % Differential chemical species variables
    a=s(1); 
    b=s(2); 
    c=s(3); 
    d=s(4); 
    e=s(5); 
    f=s(5); 

    % Differential System
    a_dt = -k1*a*b;
    b_dt = -k1*a*b + k2*d;
    c_dt =  k1*a*b        - k3*c;
    d_dt =  k1*a*b - k2*d;
    e_dt =                + k3*c;
    f_dt =                + k3*c;       
    
    dS=[a_dt,b_dt,c_dt,d_dt,e_dt,f_dt]';
end

