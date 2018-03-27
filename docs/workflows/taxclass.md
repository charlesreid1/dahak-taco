# Taxonomic Classification Walkthrough

In this document, we walk through a few 
rules in the taxonomic workflow
to illustrate how to run dahak workflows
using custom rules and custom workflow 
parameters.

See [dahak - taxonomic classification workflow](https://github.com/dahak-metagenomics/dahak/tree/master/workflows/taxonomic_classification).

## Listing Rules

Start by selecting which rule from the workflow you want to run.
To see available rules, run:

```
$ ./taco ls
```

Add the rule you want to run to the workflow configuration file.

Also see [list of rules](#list-of-rules) below.

## Rule: Pull Biocontainers

Let's start with `pull_biocontainers`, a simple example 
of a single workflow step with no input or output files. 

```text
pull_biocontainers
    
    - Pull the latest version of sourmash, kaiju, and krona
    - Version numbers are set in biocontainers.settings
    - To call this rule, ask for the file .pulled_containers
```    

To run the `pull_biocontainers` workflow:

```
$ cat pull-biocontainers-workflow.json
{
    "workflow_target" : "pull_biocontainers"
}
```

Now run the workflow (include `-n` to do a dry run):

```
$ ./taco -n pull-biocontainers-workflow # dry run

$ ./taco pull-biocontainers-workflow
```

Note that the `biocontainers` rule is defined in 
`rules/dahak/biocontainers.rule`
and the corresponding default parameter
values are defined in `rules/dahak/biocontainers.settings`.

If we wanted to modify any parameters,
we could add configuration parameters
to `pull-biocontainers-params.json`.

```
$ cat pull-biocontainers-params.json
{
    'biocontainers' : {
        'sourmash' : {
            'version' : '2.0.0a2--py36_0'
        }
    }
}
```

Now run the workflow, specifying both the workflow
and parameter configuration files on the command line
(include `-n` to do a dry run):

```
$ ./taco -n pull-biocontainers-workflow pull-biocontainers-params # dry run

$ ./taco pull-biocontainers-workflow pull-biocontainers-params
```

## Rule: Download and Unpack Sourmash SBTs

```text
download_sourmash_sbts
    
    Download the sourmash SBTs from spacegraphcats

    To call this rule, request sourmash SBT json file for the specified database.
    
unpack_sourmash_sbts
    
    Unpack the sourmash SBTs
```

Like the prior step, this step has no
input or output file names to set.

This step downloads SBTs containing hashes
from the microbial genomes in the NCBI Databank
and RefSeq databases.

```
$ cat unpack-sbt-workflow.json
{
    "workflow_target" : "unpack_sourmash_sbts"
}

$ ./taco -n unpack-sbt-workflow # dry run

$ ./taco unpack-sbt-workflow
```

This calls the `unpack_sourmash_sbts` rule,
which calls the `download_sourmash_sbts` rule.
These rules are defined in `rules/dahak/sourmash_sbt.rule`.

## Rule: Calculate Signatures (Default Parameters)

The calculate signatures rule can be run with default values:

```
$ cat calc-sigs.json
{
    "workflow_target" : "calculate_signatures"
}

$ ./taco -n calc-sigs # dry run

$ ./taco calc-sigs
```

## Rule: Calculate Signatures (Modified Parameters)

We can modify parameters for the calculate signatures workflow.

If we examine the `calculate_signatures` rule file at 
`rules/dahak/calculate_signatures.rule` we see that three
settings files are used:

* read settings (group parameters for any task involving reading sequences)
* calculate signature settings (rule-specific settings for calculating signatures)
* biocontainer settings (container URLs and versions)

We can override any parameters in those files 
to change how the `calculate_signatures` workflow
works.

**Example 1:** Change the name of the forward and reverse read files.

```
$ cat calc-sigs-params.json
{
    "reads" : {
        "fq_fwd" : "{base}_1.trim{ntrim}.fq.gz",
        "fq_rev" : "{base}_2.trim{ntrim}.fq.gz"
    }
}

$ cat calc-sigs.json
{
    "workflow_target" : "calculate_signatures"
}

$ ./taco -n calc-sigs calc-sigs-params # dry run

$ ./taco calc-sigs calc-sigs-params
```

**Example 2:** Change the k values used to calculate signatures.

```
$ cat calc-sigs-params.json
{
    "calculate_signatures" : {
        "kvalues" : [21, 31, 51, 101]
    }
}

$ cat calc-sigs.json
{
    "workflow_target" : "calculate_signatures"
}

$ ./taco -n calc-sigs calc-sigs-params # dry run

$ ./taco calc-sigs calc-sigs-params
```

**Example 3:** Change the sequence and merge file naming schema.

```
$ cat calc-sigs-params.json
{
    "calculate_signatures" : {
        "sig_name" : "{base}.trim{ntrim}.scaled{scale}.k{kvalues_fname}.sig"
    }
}
```

NOTE: `kvalues_fname` is a variable created when the rule is run,
and is the result of `"_".join(config['calculate_signatures']['kvalues'])`.

TODO: improve the abstraction.

**Example 4:** Implement all three of the above parameter changes.

```
$ cat calc-sigs-params.json
{
    "reads" : {
        "fq_fwd" : "{base}_1.trim{ntrim}.fq.gz",
        "fq_rev" : "{base}_2.trim{ntrim}.fq.gz"
    },
    "calculate_signatures" : {
        "kvalues" : [21, 31, 51, 101],
        "sig_name" : "{base}.trim{ntrim}.scaled{scale}.k{kvalues_fname}.sig"
    }
}

$ cat calc-sigs.json
{
    "workflow_target" : "calculate_signatures"
}

$ ./taco -n calc-sigs calc-sigs-params # dry run

$ ./taco calc-sigs calc-sigs-params
```

## Rule: Fetch Kaiju Database

The `unpack_kaiju` rule will fetch the kaiju database,
untar it, and remove the tar file.

This is a large file and will take approx. 15-30 minutes.

The name of the database being downloaded, and the URL, 
can be overridden using a parameters file. The default
value is shown here.

```
$ cat fetch-kaiju-params.json
{
    'kaiju' : {
        'dmp1' : 'nodes.dmp',
        'dmp2' : 'names.dmp',
        'fmi'  : 'kaiju_db_nr_euk.fmi',
        'tar'  : 'kaiju_index_nr_euk.tgz',
        'url'  : 'http://kaiju.binf.ku.dk/database',
        'out'  : '{base}.kaiju_output.trim{ntrim}.out'
    }
}

$ cat fetch-kaiju.json
{
    'workflow_target' : 'unpack_kaiju'
}

$ ./taco -d fetch-kaiju fetch-kaiju-params # dry run

$ ./taco fetch-kaiju fetch-kaiju-params
```

`kaiju.rule` includes three settings files:

* `reads` group settings
* `biocintainers` app settings
* `kaiju` app settings

## List of Rules

```text
download_sourmash_sbts
    
    Downoad the sourmash SBTs from spacegraphcats

    To call this rule, request sourmash SBT json file for the specified database.
    
unpack_sourmash_sbts
    
    Unpack the sourmash SBTs
    
calculate_signatures
    
    Calculate signatures from trimmed data using sourmash
    
download_trimmed_data
    
    Download the trimmed data from OSF

    To call this rule, request the files listed in trimmed_data.dat
    
unpack_kaiju
    
    Download and unpack the kaiju database.
    
run_kaiju
    
    Run kaiju
    
kaiju2krona
    
    Convert kaiju results to krona results,
    and generate a report.
    
kaiju2kronasummary
    
    Convert kaiju results to krona results,
    and generate a report.
    
filter_taxa_total
    
    Filter out taxa with low abundances by obtaining genera that
    comprise at least {pct} percent of the total reads
    (default: 1%)
    
filter_taxa_class
    
    For comparison, take the genera that comprise
    at least {pct} percent of all of the classified reads
    (default: 1%)
    
visualize_krona
    
    Visualize the results of the
    full and filtered taxonomic
    classifications using krona.
```    

## List of Rule Files

```
rules/
    dahak/
        biocontainers.rule
        calculate_signatures.rule
        filter_taxa.rule
        kaiju.rule
        kaiju2krona.rule
        krona_visualization.rule
        sourmash_sbt.rule
        trimmed_data.rule
```
