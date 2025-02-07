# 3 minutes to Temporian

This is a _very_ quick introduction to how Temporian works. For a complete tour of its capabilities, please refer to the [User Guide](../user_guide).

## Events and EventSets

The most basic unit of data in Temporian is an **event**. An event consists of a timestamp and a set of feature values.

Events are not handled individually. Instead, events are grouped together into an **[EventSet][temporian.EventSet]**.

[`EventSets`][temporian.EventSet] are the main data structure in Temporian, and represent **[multivariate time sequences](../user_guide/#what-is-temporal-data)**. Note that "multivariate" indicates that each event in the time sequence holds several feature values, and "sequence" indicates that the events are not necessarily sampled at a uniform rate (in which case we would call it a time "series").

You can create an [`EventSet`][temporian.EventSet] from a pandas DataFrame, NumPy arrays, CSV files, and more. Here is an example of an [`EventSet`][temporian.EventSet] containing four events and three features:

```python
>>> evset = tp.event_set(
...     timestamps=["2023-02-04", "2023-02-06", "2023-02-07", "2023-02-07"],
...     features={
...         "feature_1": [0.5, 0.6, np.nan, 0.9],
...         "feature_2": ["red", "blue", "red", "blue"],
...         "feature_3":  [10.0, -1.0, 5.0, 5.0],
...     },
...     indexes=["feature_2"],
... )

```

An [`EventSet`][temporian.EventSet] can hold one or several time sequences, depending on what its **[index](../user_guide/#index-horizontal-and-vertical-operators)** is.

If the [`EventSet`][temporian.EventSet] has no index, it will hold a single time sequence, which means that all events will be considered part of the same group and will interact with each other when operators are applied to the [`EventSet`][temporian.EventSet].

If the [`EventSet`][temporian.EventSet] has one (or many) indexes, it will hold one time sequence for each unique value (or unique combination of values) of the indexes, the events will be grouped by their index key, and operators applied to the [`EventSet`][temporian.EventSet] will be applied to each time sequence independently.

## Graph, EventSetNodes, and Operators

There are two big phases in any Temporian script: graph **definition** and **evaluation**. This is a common pattern in computing libraries, and it allows us to perform optimizations before the graph is run, share Temporian programs across different platforms, and more.

A graph is created by using **operators**. For example, the [`tp.simple_moving_average()`][temporian.simple_moving_average] operator computes the [simple moving average](https://en.wikipedia.org/wiki/Moving_average) of each feature in an [`EventSet`][temporian.EventSet]. You can find documentation for all available operators [here](../reference/).

Note that when calling operators you are only defining the graph - i.e., you are telling Temporian what operations you want to perform on your data, but those operations are not yet being performed.

Operators are not applied directly to [`EventSets`][temporian.EventSet], but to **[EventSetNodes][temporian.EventSetNode]**. You can think of an [`EventSetNode`][temporian.EventSetNode] as the placeholder for an [`EventSet`][temporian.EventSet] in the graph. When applying operators to [`EventSetNodes`][temporian.EventSetNode], you get back new [`EventSetNodes`][temporian.EventSetNode] that are placeholders for the results of those operations. You can create arbitrarily complex graphs by combining operators and [`EventSetNodes`][temporian.EventSetNode].

```python
>>> # Obtain the EventSetNode corresponding to the EventSet we created above
>>> source = evset.node()
>>>
>>> # Apply operators to existing EventSetNodes to generate new EventSetNodes
>>> addition = source["feature_1"] + source["feature_3"]
>>> addition_lagged = tp.lag(addition, duration=tp.duration.days(7))

```

<!-- TODO: add image of the generated graph -->

Your graph can now be run by calling [`.run()`][temporian.EventSetNode.run] on any [`EventSetNode`][temporian.EventSetNode] in the graph, which will perform all necessary operations and return the resulting [`EventSet`][temporian.EventSet].

```python
>>> result = addition_lagged.run(evset)

```

Note that you need to pass the [`EventSets`][temporian.EventSet] that correspond to the source [`EventSetNodes`][temporian.EventSetNode] in the graph to [`.run()`][temporian.EventSetNode.run] (since those are not part of the graph definition). Also, several [`EventSetNodes`][temporian.EventSetNode] can be run at the same time by calling [`tp.run()`][temporian.run] directly.

🥳 Congratulations! You're all set to write your first pieces of Temporian code.

For a more in-depth look at Temporian's capabilities, please check out the [User Guide](../user_guide) or some of the use cases in the [Tutorials](../tutorials) section.
