# Examples for using `uproot` and `awkward-array`

Here, we have a few examples for using `awkward` arrays with
`uproot`. Once you have this package installed, then execute:

```
docker pull srappoccio/scikit-hep-examples:latest
```

To execute, ensure that you have a directory called `results` parallel
to this one:

```
mkdir ../results
```

Then, execute:

```
./runDockerX11OSX.sh srappoccio/scikit-hep-examples
```

**Finally, you will have several notebooks in that directory. Copy
them to the `results` directory, or else they will be deleted when the
docker image exits.**
