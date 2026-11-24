package status

import (
	"reflect"
	"strings"
	"testing"
)

func TestParseNvidia(t *testing.T) {
	input := "NVIDIA RTX 3060, 12288\ninvalid\n\"GPU, B\", [N/A]\n, 5\n"
	want := []GPU{{Name: "NVIDIA RTX 3060", VRAMMB: 12288}, {Name: "GPU, B"}}
	if got := parseNvidia(strings.NewReader(input)); !reflect.DeepEqual(got, want) {
		t.Fatalf("GPUs = %#v, want %#v", got, want)
	}
	if got := parseNvidia(strings.NewReader("")); got == nil || len(got) != 0 {
		t.Fatalf("empty GPU list = %#v", got)
	}
}

func TestBoundModelName(t *testing.T) {
	if got := modelName(strings.Repeat("π", 200)); got != strings.Repeat("π", 128) {
		t.Fatal("incorrect length for Unicode name")
	}
	if got := modelName("\xff"); got != "" {
		t.Fatalf("invalid UTF-8 name = %q", got)
	}
}
