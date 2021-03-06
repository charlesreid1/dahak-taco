## priorities

(note: this will be transitioning into [dahak-taco issues](https://github.com/dahak-metagenomics/dahak-taco/issues))

### installation

Checking to ensure Snakemake/singularity/conda installed

(See issues)


### improving output/input file specification

Example of a ghost "make all" style rule:

* [here](https://github.com/spacegraphcats/spacegraphcats/blob/extract_reads_contigs_rules/conf/Snakefile#L218)
* requests outputs as inputs, requests no outputs, defines no rule
* apply it to hello/time/goodbye rules


### workflow caboose

add a notifications caboose:

* print notifications of where stuff is 
* send notifications via mail() calls, API calls, webhooks, etc.

email specifically?

* ubuntu sendmail container
* php + mail() (apache not necesary - php script from command line)
* https://www.abeautifulsite.net/configuring-sendmail-on-ubuntu-1404


### imporovements to cli

many issues open on these topics. mainly:

* improving logic and simplifying
* restructure to take advantage of ghost all rule
* yaml and json extensions can be automatically detected


### prefix location

Prefix location with `--prefix`


### parameter presets

issue opened detailing various options


### `taco validate`

among the many improvements planned.

This takes an optional config and/or params argument and validates it.

```
taco validate --help

taco validate --config=goodies/w1config.json

taco validate --params=goodies/w1config.json

taco validate \
    --config=goodies/w1config.json \
    --params=goodies/w1params.json
```


## rules

* Tab completion


## walkthrus

Read filtering walkthrough:

* Revisit
* Rewrite:
    * We have to define all the parameters
    * We can define one preset to demonstrate how to do it


## done

Done:

* <s>finish read trim workflow</s>
* <s>finish read trim walkthru</s>
* <s>custom dockerfile/image in place of quay url</s>

<s>uh oh... huge problem.
    
* scenario: we provided values, but not at the right place
* the dict keys we defined are never used
* the default dict keys are used instead
* add a --clean option so we don't use any default parameters
* only useful for testing.</s>

More Done:

* <s>make the program more robust to errors or misconfiguration</s> (see --clean)

<s>requirements (see scripts/ folder, or [dahak-yeti](https://github.com/charlesreid1/dahak-yeti)):</s>
    
* <s>fix pyenv installation script
* fix conda installation script 
* fix snakemake installation script
* fix singularity installation script</s>

Yet another thing we can't do, because Snakemake:

* <s>Common tasks/rules: common workflow folder? (e.g., pull biocontainers rule)</s>
* <s>Tried putting utils in a common workflow dir. FAILED TO IMPORT</s> 
* <s>Tried putting utils in the workflow dir. FAILED TO IMPORT</s>
* Literally the only thing that works is making a copy of utils.py in every single workflow directory. 
* The problem 

more:

* <s>start a (very long) list of all the land mines I discovered in Snakemake</s>

* <s>file name and extension and parameter validation: implement where needed
* validation should occur *within* the rule
* we want the user to know which rule caused the problem</s>

"Validation should occur *within* the rule" is precisely the heart of the problem:
Snakemake separately evalutes non-rule Python code, then evaluates rules.
If you validate inside a rule, you can't validate inputs, outputs, singularity containers,
or anything else but the `run` block.

### documentation

<s>developers guide:
    
* making new rules
* creating a default parameter set</s>


### yaml

<s>switch input from json to yaml</s>

<s>important:
    
* create an input config validator
* this adds yet another action to dahak...
* which one is easier?</s>

<s>What else?
    
* get the read filtering workflow back up an running
* tag the next release 
* add a changelog
* the idiotic problem of not being able to import things...</s>

<s>prefix:
    
* clear up ambiguity about data/ prefix.
* does the user specify it in filenames, or not? clear this up.
    * right now:
    * in the params dictionary, the user does not specify `data/` prefix.
    * config and rule targets, yes, the user must specify `data/` prefix.</s>


### tests

<s>tests:
    
* taco cl usage tests
* taco workflow tests</s>


## taco cli

<s>
* add common parser: [link](https://github.com/dcppc/dcppc-bot/pull/4/files#diff-d51593b709dedb0cfd088f88515df1a2R180)

* improve the command line interface

```
Usage:
taco <action> [OPTIONS]

    Actions:
        
        taco help           Print long help message
        taco ls             List workflows 
        taco ls <workflow>  List rules in workflow <workflow>
        taco validate       Validate input JSON/YAML
        taco <workflow>     Run workflow <workflow>
```
</s>


### `taco ls`

<s>To list all workflows that are available:

```
taco ls
```

Once you decide on a workflow, you can list all rules
in that workflow and get a brief description of each:

```
taco ls --help

taco ls

taco ls <workflow>
```
</s>


### `taco <workflow>`

<s>The meat of the taco, the workflows take two arguments:
the config file and the params file.

Here are some example usages of the workflow commands:

```
taco workflow1 --help

taco workflow1 --config=goodies/w1config.json \
               --params=goodies/w1config.json
```
</s>

## documentation

<s>Users:

* Mention `data_dir` parameter and "where's my stuff"
* Mention logs, output, and troubleshooting information
* How to change other rules and settings

Dev:

* Add new rule
* Structuring rules
* docker singularity biocontainers bioconda</s>

Note: some of these todos are not finished but have been moved to other repositories (taco-simple, taco-read-filtering, etc.)


