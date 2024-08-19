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

```shell
git submodule update --init --recursive
```

If you don’t want to see the extra agent framework code, you can run:

```shell
cd aios/sdk/autogen

git sparse-checkout init --cone

git sparse-checkout set autogen
```

or simply run on linux or mac:

```shell
sh init_autogen.sh
```