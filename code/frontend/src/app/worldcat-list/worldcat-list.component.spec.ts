import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WorldcatListComponent } from './worldcat-list.component';

describe('WorldcatListComponent', () => {
  let component: WorldcatListComponent;
  let fixture: ComponentFixture<WorldcatListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WorldcatListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WorldcatListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
