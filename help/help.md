% {{ spec.image_name }} (1) Container Image Pages
% Tomas Tomecek
% September 11th, 2017

# NAME
tools - container with all the management tools you miss in Atomic Host


# DESCRIPTION
You find plenty of well-known tools within this container. Here comes the full list:

{{ spec.tools_table }}

# USAGE
You should invoke this container using `atomic` command:

```
$ atomic run {{ spec.repository }}
```


# SECURITY IMPLICATIONS
This container runs as a super-privileged container: it has full root access.


# HISTORY
Release 1: initial release
