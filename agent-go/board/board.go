// Package board derives a deterministic task board from verified records.
package board

import (
	"fmt"
	"slices"
	"sort"
	"strings"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
)

type Object = config.Object

func Body(e Object) Object    { return config.Obj(e["body"]) }
func Payload(e Object) Object { return config.Obj(Body(e)["payload"]) }
func Created(e Object) int64  { return config.Num(Body(e)["created"], 0) }
func ID(e Object) string      { return config.Str(e["id"]) }
func Author(e Object) string  { return config.Str(Body(e)["author"]) }
func Kind(e Object) string    { return config.Str(Body(e)["type"]) }
func Handover(e Object) int64 { return Created(e) + config.Num(Payload(e)["handover_days"], 14)*86400 }
func Rank(task Object, author string, created, now int64) int {
	if Author(task) == author {
		return 2
	}
	handover := Handover(task)
	if now < handover || created < handover {
		return 0
	}
	deputies, _ := Payload(task)["deputies"].([]any)
	if slices.Contains(deputies, any(author)) {
		return 1
	}
	return 0
}

type Info struct {
	Task            Object
	Claims, Reports []Object
	Verdicts        map[string]Object
	Accepted        []string
}

func (i *Info) Status() string {
	switch {
	case len(i.Accepted) > 0:
		return "accepted"
	case len(i.Reports) > 0:
		return "reported"
	case len(i.Claims) > 0:
		return "claimed"
	}
	return "open"
}
func Build(entries []Object, now int64) map[string]*Info {
	tasks := map[string]*Info{}
	byID := map[string]Object{}
	ordered := slices.Clone(entries)
	sort.Slice(ordered, func(i, j int) bool {
		a, b := ordered[i], ordered[j]
		if Created(a) != Created(b) {
			return Created(a) < Created(b)
		}
		return ID(a) < ID(b)
	})
	latest := map[[2]string]string{}
	for _, e := range ordered {
		byID[ID(e)] = e
		switch Kind(e) {
		case "task":
			tasks[ID(e)] = &Info{e, []Object{}, []Object{}, map[string]Object{}, []string{}}
		case "claim":
			latest[[2]string{config.Str(Payload(e)["task"]), Author(e)}] = ID(e)
		}
	}
	for _, e := range ordered {
		p := Payload(e)
		t := config.Str(p["task"])
		info := tasks[t]
		if info == nil {
			continue
		}
		switch Kind(e) {
		case "claim":
			until := config.Num(p["until"], 0)
			if latest[[2]string{t, Author(e)}] == ID(e) && now < until && until <= Created(e)+30*86400 {
				info.Claims = append(info.Claims, e)
			}
		case "report":
			info.Reports = append(info.Reports, e)
		case "accept", "revise":
			rid := config.Str(p["report"])
			report := byID[rid]
			if Kind(report) != "report" || Payload(report)["task"] != t || Created(e) < Created(report) {
				continue
			}
			rank := Rank(info.Task, Author(e), Created(e), now)
			prev := info.Verdicts[rid]
			if rank > 0 && (prev == nil || rank >= Rank(info.Task, Author(prev), Created(prev), now)) {
				info.Verdicts[rid] = e
			}
		}
	}
	for _, i := range tasks {
		for rid, e := range i.Verdicts {
			if Kind(e) == "accept" {
				i.Accepted = append(i.Accepted, rid)
			}
		}
		sort.Strings(i.Accepted)
	}
	return tasks
}
func Find(records []Object, prefix, kind string) (Object, error) {
	prefix = strings.ToLower(prefix)
	if len(prefix) < 6 {
		return nil, fmt.Errorf("give at least 6 characters of the id")
	}
	var found Object
	for _, e := range records {
		if (kind == "" || Kind(e) == kind) && strings.HasPrefix(ID(e), prefix) {
			if found != nil {
				return nil, fmt.Errorf("several records start with %s; give more characters", prefix)
			}
			found = e
		}
	}
	if found == nil {
		return nil, fmt.Errorf("no matching record with an id starting with %s (try: skynet-agent net sync)", prefix)
	}
	return found, nil
}
