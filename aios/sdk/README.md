# SDK

## Introduction
This repository contains an agent framework,
which has been modified to run on AIOS based on the existing agent framework.

contains
- autogen

## Start

### autogen

If you want to use sdk, 
you shoud initiate it by running following code.

If you do not need to make changes to autogen, you can save more space by using a shallow clone:

```shell
sh init_autogen_shallow.sh
```

If you want a complete commit history of autogen, please run:
```shell
sh init_autogen.sh
```

Or you can init autogen by hand:

```shell
git submodule update --init --recursive

cd aios/sdk/autogen

git sparse-checkout init --cone

git sparse-checkout set autogen
```